from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_s3 as s3, Duration,
    aws_stepfunctions as stepfunctions,
    aws_stepfunctions_tasks as stepfunctions_tasks,
)
from constructs import Construct


class IacStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        s3_bucket = s3.Bucket(
            self, "s3-bucket",
            bucket_name="rental-data-fetcher-bucket",
            versioned=True,
            encryption=s3.BucketEncryption.KMS_MANAGED,
            enforce_ssl=True,
        )

        fetch_zumper_data_lambda = lambda_.DockerImageFunction(
            self, "fetch_zumper_data",
            function_name="FetchZumperDataFunction",
            code=lambda_.DockerImageCode.from_image_asset(
                directory="./src"
            ),
            environment={
                "S3_BUCKET_NAME": s3_bucket.bucket_name,
                "JOBLIB_MULTIPROCESSING": "0"
            },
            memory_size=1024,
            timeout=Duration.seconds(900),
        )

        s3_bucket.grant_write(fetch_zumper_data_lambda)

        state_machine = stepfunctions.StateMachine(
            self, "state-machine",
            state_machine_name="ZumperDataStateMachine",
            definition=stepfunctions_tasks.LambdaInvoke(
                self, "fetc-zumper-data-lambda-invoke",
                lambda_function=fetch_zumper_data_lambda).next(
                stepfunctions.Succeed(self, "Success")
            )
        )
