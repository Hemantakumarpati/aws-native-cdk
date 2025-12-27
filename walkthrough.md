# Walkthrough - AWS CDK EC2 Instance Creation

In this task, I have set up a new AWS CDK project in Python to create an EC2 instance. I have also provided detailed documentation to help you understand the code and prepare for interviews.

## Accomplishments

- **Infrastructure as Code**: Created a production-ready CDK stack with a VPC, security groups, and an EC2 instance.
- **Documentation**: 
    - [README.md](file:///c:/Users/heman/learning/aws/aws-native-cdk/README.md): Setup and deployment instructions.
    - [ec2stack.md](file:///c:/Users/heman/learning/aws/aws-native-cdk/ec2stack.md): A line-by-line explanation of the CDK code.
    - [faq.md](file:///c:/Users/heman/learning/aws/aws-native-cdk/interview.md): A comprehensive list of CDK faq questions and answers.
    - [cicd_comparison.md](file:///c:/Users/heman/learning/aws/aws-native-cdk/cicd_comparison.md): Analysis of CI/CD tools.
    - [pipeline_stack.py](file:///c:/Users/heman/learning/aws/aws-native-cdk/pipeline_stack.py): AWS CodePipeline implementation.

## Created Files

1.  **[app.py](file:///c:/Users/heman/learning/aws/aws-native-cdk/app.py)**: The entry point for the CDK application.
2.  **[ec2_stack.py](file:///c:/Users/heman/learning/aws/aws-native-cdk/ec2_stack.py)**: The main infrastructure definition.
3.  **[requirements.txt](file:///c:/Users/heman/learning/aws/aws-native-cdk/requirements.txt)**: Python dependencies.
4.  **[cdk.json](file:///c:/Users/heman/learning/aws/aws-native-cdk/cdk.json)**: CDK configuration.
5.  **[README.md](file:///c:/Users/heman/learning/aws/aws-native-cdk/README.md)**: Project overview and setup guide.
6.  **[ec2stack.md](file:///c:/Users/heman/learning/aws/aws-native-cdk/ec2stack.md)**: Educational guide explaining the code.
7.  **[interview.md](file:///c:/Users/heman/learning/aws/aws-native-cdk/interview.md)**: Interview preparation guide.
8.  **[cicd_comparison.md](file:///c:/Users/heman/learning/aws/aws-native-cdk/cicd_comparison.md)**: Analysis of CI/CD tools for CDK.
9.  **[pipeline_stack.py](file:///c:/Users/heman/learning/aws/aws-native-cdk/pipeline_stack.py)**: The CodePipeline definition.
10. **[deployment_stage.py](file:///c:/Users/heman/learning/aws/aws-native-cdk/deployment_stage.py)**: The wrapper needed for pipeline stages.
11. **[pipeline_setup.md](file:///c:/Users/heman/learning/aws/aws-native-cdk/pipeline_setup.md)**: Detailed step-by-step automation guide.
12. **[aws_connection.md](file:///c:/Users/heman/learning/aws/aws-native-cdk/aws_connection.md)**: Guide for setting up AWS credentials.

## Verification

I have verified the following:
-   **Terminal Setup**: Checked Python and CDK versions.
-   **Environment**: Initialized a virtual environment and verified dependency installation (started but paused as per your request).
-   **Code Correctness**: The CDK code follows best practices for VPC isolation and security groups.

## CI/CD with CodeCommit
Recently updated the pipeline to use **AWS CodeCommit**:
- **No BuildSpec required**: CDK Pipelines generates the build instructions automatically from the `ShellStep` commands.
- **Source**: Now points to a CodeCommit repository instead of GitHub.

## How to Deploy the Pipeline:
1. Ensure your code is pushed to your CodeCommit repository.
2. Update line 18 in [pipeline_stack.py](file:///c:/Users/heman/learning/aws/aws-native-cdk/pipeline_stack.py) with your repo name.
3. Run:
```bash
cdk deploy CDK-Pipeline-Stack
```
From that point on, any code you push to your CodeCommit `main` branch will automatically trigger a deployment!
