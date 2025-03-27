from aws_cdk import (
    Duration,
    aws_s3 as s3,
    aws_s3_deployment as s3_deployment,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_certificatemanager as acm,
    aws_route53 as route53,
    aws_route53_targets as targets,
    aws_ssm as ssm,
    RemovalPolicy,
)
from constructs import Construct

from ..shared.base_stack import BaseStack
from ..shared.paths import WEB_DIST_PATH

class WebStack(BaseStack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(
            self, "web-bucket", bucket_name="www-wild-west",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        bucket_deployment = s3_deployment.BucketDeployment(
            self, "bucket-deployment", destination_bucket=bucket,
            sources=[s3_deployment.Source.asset(WEB_DIST_PATH)]
        )

        cert_arn = ssm.StringParameter.value_for_string_parameter(self, "wild-west-ssl-cert")
        cert = acm.Certificate.from_certificate_arn(self, "ssl-cert", cert_arn)
        cf = cloudfront.Distribution(
            self, "cf-distribution",
            default_root_object="index.html",
            certificate=cert,
            domain_names=["wildwestdentrepair.com", "www.wildwestdentrepair.com"],
            default_behavior={
                "origin": origins.S3Origin(bucket),
                "viewer_protocol_policy": cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
            },
            error_responses=[
                cloudfront.ErrorResponse(
                    http_status=404,
                    response_http_status=200,
                    response_page_path="/",
                    ttl=Duration.minutes(30)
                ),
                cloudfront.ErrorResponse(
                    http_status=403,
                    response_http_status=200,
                    response_page_path="/",
                    ttl=Duration.minutes(30)
                )
            ]
        )

        zone_id = ssm.StringParameter.value_for_string_parameter(self, "wild-west-hosted-zone-id")
        hosted_zone = route53.HostedZone.from_hosted_zone_attributes(
            self, "hosted-zone",
            hosted_zone_id=zone_id,
            zone_name="wildwestdentrepair.com"
        )
        
        www_record = route53.ARecord(
            self, "www-a-record", zone=hosted_zone,
            record_name="www.wildwestdentrepair.com",
            target=route53.RecordTarget.from_alias(targets.CloudFrontTarget(cf))
        )
        record = route53.ARecord(
            self, "a-record", zone=hosted_zone,
            record_name="wildwestdentrepair.com",
            target=route53.RecordTarget.from_alias(targets.CloudFrontTarget(cf))
        )