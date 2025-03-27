import os

import aws_cdk as cdk
from constructs import Construct

DEPLOY_ENV = os.getenv("DEPLOY_ENV", "dev")

cdk_env = cdk.Environment(
    account="798834959369",
    region="us-east-1"
)

class BaseStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        self.construct_id = f"{construct_id}-{DEPLOY_ENV}"
        self.stack_prefix = DEPLOY_ENV

        super().__init__(scope, self.construct_id, env=cdk_env, **kwargs)
