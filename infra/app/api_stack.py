import os

from aws_cdk import (
    Fn,
    aws_certificatemanager as acm,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_iam,
    aws_route53 as route53,
    aws_route53_targets as targets,
    aws_ssm as ssm,
    aws_lambda 
)
from constructs import Construct

from ..shared.base_stack import BaseStack
from ..shared.paths import API_PATH
layer_path = os.path.join(API_PATH, "layer")

class ApiStack(BaseStack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_layer = aws_lambda.LayerVersion(
            self, "external-layer", code=aws_lambda.Code.from_asset(layer_path),
            compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_11]
        )

        function = aws_lambda.Function(
            self, "wild-west-api",
            code=aws_lambda.Code.from_asset(API_PATH, exclude=["layer", "__pycache__", ".venv"]),
            handler="main.handler",
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            layers=[lambda_layer],
            architecture=aws_lambda.Architecture.ARM_64
        )

        function.add_to_role_policy(aws_iam.PolicyStatement(
            actions=[
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "logs:CreateLogGroup",
            ],
            resources= ['*'],
            effect= aws_iam.Effect.ALLOW
        ))

        function.add_to_role_policy(aws_iam.PolicyStatement(
            actions=['ses:SendEmail', 'ses:SendRawEmail'],
            resources= ['*'],
            effect= aws_iam.Effect.ALLOW
        ))
        function_url = function.add_function_url(
            auth_type=aws_lambda.FunctionUrlAuthType.NONE,
            cors=aws_lambda.FunctionUrlCorsOptions(
                allowed_origins=["*"],
                allowed_methods=[aws_lambda.HttpMethod.ALL],
                exposed_headers=[
                    "access-control-allow-origin",
                    "access-control-allow-methods", 
                    "access-control-allow-header",
                    "access-control-allow-credentials",
                    "access-control-max-age"
                ],
                allowed_headers=["content-type", "access-control-allow-origin",
                    "access-control-allow-methods", 
                    "access-control-allow-header",
                    "access-control-allow-credentials",
                    "access-control-max-age"]
            )
        )

        cert_arn = ssm.StringParameter.value_for_string_parameter(self, "wild-west-ssl-cert")
        cert = acm.Certificate.from_certificate_arn(self, "ssl-cert", cert_arn)
        cf = cloudfront.Distribution(
            self, "cf-distribution",
            certificate=cert,
            domain_names=["api.wildwestdentrepair.com"],
            default_behavior={
                "origin": origins.HttpOrigin(Fn.select(2, Fn.split('/', function_url.url))),
                "viewer_protocol_policy": cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                "allowed_methods":cloudfront.AllowedMethods.ALLOW_ALL,
                "cache_policy":cloudfront.CachePolicy.CACHING_DISABLED
            }
        )

        zone_id = ssm.StringParameter.value_for_string_parameter(self, "wild-west-hosted-zone-id")
        hosted_zone = route53.HostedZone.from_hosted_zone_attributes(
            self, "hosted-zone",
            hosted_zone_id=zone_id,
            zone_name="wildwestdentrepair.com"
        )
        
        www_record = route53.ARecord(
            self, "api-a-record", zone=hosted_zone,
            record_name="api.wildwestdentrepair.com",
            target=route53.RecordTarget.from_alias(targets.CloudFrontTarget(cf))
        )
    