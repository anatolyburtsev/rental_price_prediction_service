import json
import aws_cdk as cdk
from constructs import Construct

from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_s3 as s3,
    aws_secretsmanager as sm,
    aws_iam as iam,
    aws_dynamodb as dynamodb
)


class FargateStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Retrieve the first public subnet available in the default VPC in the AWS account.
        # The subnet ID will be used to run a task
        fargate_vpc = ec2.Vpc.from_lookup(self, "Vpc", is_default=True)
        public_subnet = fargate_vpc.public_subnets[0]

        fargate_cluster = ecs.Cluster(self, "FetchDataCluster", cluster_name="FetchDataCluster", vpc=fargate_vpc)

        # Create Fargate Execution Role
        fargate_role = iam.Role(
            self, "FargateTaskExecutionRole",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            description="Fargate Task Execution Role",
        )

        fargate_task_def = ecs.FargateTaskDefinition(
            self, "FetchDataTaskDef",
            memory_limit_mib=512,
            cpu=256,
            execution_role=fargate_role
        )

        s3_bucket = s3.Bucket(self, 'fetchedDataBucket', bucket_name="zumperdata")
        s3_bucket.grant_write(fargate_task_def.task_role)
        s3_bucket.grant_write(fargate_task_def.execution_role)

        fargate_container = fargate_task_def.add_container(
            "WGMidDataContainer",
            image=ecs.ContainerImage.from_asset("./src"),
            memory_limit_mib=512,
            logging=ecs.LogDrivers.aws_logs(stream_prefix="FetchDataLogs"),
            # Secrets are retrieved from AWS Secrets Manager at container start-up
            secrets={
            },
            environment={
            },
            command=["python3", "fetch_data.py", "--destination", "s3", "--s3_path", f"s3://{s3_bucket.bucket_name}",
                     "-fpo"],
        )

        # Print out resource names/ARNs for use in testing
        cdk.CfnOutput(self, "TaskDefinitionName", description="Name of Fargate Task Definition with version",
                      value=fargate_task_def.task_definition_arn)
        cdk.CfnOutput(self, "Cluster", description="Cluster to run Fargate Tasks", value=fargate_cluster.cluster_name)
        cdk.CfnOutput(self, "Task Run Subnet", description="Subnet to run Fargate Tasks", value=public_subnet.subnet_id)
