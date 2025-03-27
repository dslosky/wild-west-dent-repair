from aws_cdk import (
    aws_route53 as route53,
    aws_certificatemanager as acm,
    aws_ssm as ssm,
    RemovalPolicy
)
from constructs import Construct

from ..shared.base_stack import BaseStack
from ..shared import globals

class HostedZoneStack(BaseStack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        zone = route53.HostedZone.from_lookup(
            self, 
            'HostedZone',
            domain_name=globals.DOMAIN_NAME
        )

        cert = acm.Certificate(self, 'Certificate',
        domain_name=globals.DOMAIN_NAME,
        subject_alternative_names=[f"*.{globals.DOMAIN_NAME}"],
        certificate_name= 'wild west dent repair',
        validation=acm.CertificateValidation.from_dns(zone),
        )

        cert.apply_removal_policy(RemovalPolicy.DESTROY)

        hz_param = ssm.StringParameter(
            self, "hosted-zone-param",
            string_value=zone.hosted_zone_id,
            parameter_name="wild-west-hosted-zone-id"
        )
        cert_param = ssm.StringParameter(
            self, "cert-param",
            string_value=cert.certificate_arn,
            parameter_name="wild-west-ssl-cert"
        )

        # Add smtp inbox forwarding
        mx1 = route53.MxRecord(
            self, "mx1",
            values=[
                route53.MxRecordValue(
                    host_name="mx1.improvmx.com.",
                    priority=10),
                route53.MxRecordValue(
                    host_name="mx2.improvmx.com.",
                    priority=20),
            ],
            zone=zone,
        )

        txt = route53.TxtRecord(
            self, "txt-record",
            zone=zone,
            values=["v=spf1 include:spf.improvmx.com ~all"]
        )
