#!/usr/bin/env python3
import aws_cdk as cdk

from .hosted_zone_stack import HostedZoneStack


app = cdk.App()
HostedZoneStack(app, "HostedZoneStack")

cdk.Tags.of(app).add("project", "wild west")
app.synth()
