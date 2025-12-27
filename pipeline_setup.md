# Step-by-Step Guide: Creating Your Automated CI/CD Pipeline

Follow these steps to move your local CDK code into a fully automated AWS CodePipeline.

## 1. Create the CodeCommit Repository
First, create a place for your code to live in AWS.

```bash
aws codecommit create-repository --repository-name my-cdk-repo --repository-description "CDK Pipeline Repo"
```

## 2. Push Your Code to CodeCommit
Initialize git and push your project.

```bash
git init
git add .
git commit -m "Initial commit"
# Replace with your actual CodeCommit URL
git remote add origin https://git-codecommit.REGION.amazonaws.com/v1/repos/my-cdk-repo
git push -u origin main
```

## 3. Bootstrap your AWS Account
CDK needs special resources (S3 bucket, IAM roles) to manage deployments. 

```bash
cdk bootstrap
```

## 4. The "One-Time" Manual Deploy
You must deploy the pipeline stack manually **just once**. This "seeds" the pipeline in AWS.

```bash
cdk deploy CDK-Pipeline-Stack
```

## 5. Watch the Magic Happen (Self-Mutation)
From this point on, you **never** need to run `cdk deploy` from your computer again.

1.  Make a change to your code (e.g., add a new rule in `ec2_stack.py`).
2.  `git add .`
3.  `git commit -m "Update security rules"`
4.  `git push origin main`

**CodePipeline will automatically:**
-   Detect the change.
-   Start a **CodeBuild** job to run `cdk synth`.
-   **Self-Mutate**: If you changed the pipeline itself, it updates the pipeline first!
-   **Deploy**: CloudFormation will update your EC2 instance automatically.

---

## 🔍 How to Monitor Your Pipeline
1.  Go to the **AWS Console**.
2.  Search for **CodePipeline**.
3.  Look for the pipeline named `EC2-Deploy-Pipeline-CodeCommit`.
4.  You can see the status of the **Source**, **Build (Synth)**, and **Deploy** stages in real-time.

---

## 💡 Key Concept: Why no BuildSpec?
In `pipeline_stack.py`, notice the `commands` section:
```python
commands=[
    "npm install -g aws-cdk",
    "pip install -r requirements.txt",
    "cdk synth"
]
```
CDK uses these commands to **automatically generate** the `buildspec.yml` file for CodeBuild. You don't have to manage it yourself!
