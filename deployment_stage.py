import aws_cdk as cdk
from constructs import Construct
from ec2_stack import EC2Stack

class DeploymentStage(cdk.Stage):
    """
    A CDK Stage that wraps our EC2 Stack.
    This allows cdk-pipelines to deploy the stack as a unit.
    """
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Instantiate our EC2 Stack within this stage
        EC2Stack(self, "EC2-Deployment",
            description="Production EC2 Instance Deployment"
        )
