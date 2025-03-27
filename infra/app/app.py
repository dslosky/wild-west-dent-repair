#!/usr/bin/env python3
import os

import aws_cdk as cdk

from .web_stack import WebStack
from .api_stack import ApiStack

app = cdk.App()
WebStack(app, "WebStack")
ApiStack(app, "ApiStack")

cdk.Tags.of(app).add("project", "wild west")
app.synth()
