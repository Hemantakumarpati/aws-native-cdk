from aws_cdk import (
    Stack,
    pipelines,
    aws_codecommit as codecommit
)
from constructs import Construct
from deployment_stage import DeploymentStage

class PipelineStack(Stack):
    """
    CDK Stack that defines the self-mutating CodePipeline using CodeCommit.
    """
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1. Reference your existing CodeCommit repository
        # Replace 'my-cdk-repo' with your actual repository name
        repo = codecommit.Repository.from_repository_name(
            self, "ImportedRepo",
            "my-cdk-repo"
        )

        # 2. Define the Pipeline
        # Note: You do NOT need a buildspec.yml file!
        # CDK Pipelines generates it automatically from the 'commands' below.
        pipeline = pipelines.CodePipeline(
            self, "CDK-Pipeline",
            pipeline_name="EC2-Deploy-Pipeline-CodeCommit",
            synth=pipelines.ShellStep(
                "Synth",
                input=pipelines.CodePipelineSource.code_commit(repo, "main"),
                commands=[
                    "npm install -g aws-cdk",
                    "pip install -r requirements.txt",
                    "cdk synth"
                ]
            )
        )

        # 3. Add the Deployment Stage
        deploy = DeploymentStage(self, "Deploy")
        pipeline.add_stage(deploy)
