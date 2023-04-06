import aws_cdk as cdk
import os

cdk_env = cdk.Environment(
    region=os.environ["CDK_DEFAULT_REGION"],
    account=os.environ["CDK_DEFAULT_ACCOUNT"]
)