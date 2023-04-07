from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_s3 as s3, Duration,
    aws_stepfunctions as stepfunctions,
    aws_stepfunctions_tasks as stepfunctions_tasks,
    aws_iam as iam,
    aws_scheduler as scheduler,
)
import json
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
                self, "fetch-zumper-data-lambda-invoke",
                lambda_function=fetch_zumper_data_lambda).next(
                stepfunctions.Succeed(self, "Success")
            )
        )

        ## Add scheduler permissions
        scheduler_role = iam.Role(
            self, "scheduler-role",
            assumed_by=iam.ServicePrincipal("scheduler.amazonaws.com"),
        )

        scheduler_sf_execution_policy = iam.PolicyStatement(
            actions=["states:StartExecution"],
            resources=[state_machine.state_machine_arn],
            effect=iam.Effect.ALLOW,
        )

        scheduler_role.add_to_policy(scheduler_sf_execution_policy)

        ## Add schedule group
        schedule_group = scheduler.CfnScheduleGroup(
            self, "zumper-data-schedule-group",
            name="zumper-data-schedule-group",
        )

        ## Add schedule
        fetch_zumper_data_schedule = scheduler.CfnSchedule(
            self, "fetch-zumper-data-schedule",
            flexible_time_window=scheduler.CfnSchedule.FlexibleTimeWindowProperty(
                mode="OFF",
            ),
            schedule_expression="rate(1 hours)",
            group_name=schedule_group.name,
            target=scheduler.CfnSchedule.TargetProperty(
                arn=state_machine.state_machine_arn,
                role_arn=scheduler_role.role_arn,
                input=json.dumps({
                    "metadata": {
                        "eventId": "MY_SCHEDULED_EVENT",
                    },
                })
            )
        )
