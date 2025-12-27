from ec2_stack import EC2Stack
from pipeline_stack import PipelineStack

app = cdk.App()

# 1. For direct deployment (Local)
EC2Stack(app, "EC2Stack-Local",
    env=cdk.Environment(
        account=app.node.try_get_context("account"),
        region=app.node.try_get_context("region") or "us-east-1"
    ),
    description="Local EC2 Instance Deployment"
)

# 2. For Automated Pipeline Deployment
PipelineStack(app, "CDK-Pipeline-Stack",
    env=cdk.Environment(
        account=app.node.try_get_context("account"),
        region=app.node.try_get_context("region") or "us-east-1"
    ),
    description="Self-mutating CI/CD Pipeline for EC2"
)

app.synth()
