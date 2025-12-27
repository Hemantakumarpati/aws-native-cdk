# AWS CDK Interview Preparation Guide

This guide contains common and advanced interview questions you might face during a customer or technical interview focused on AWS CDK.

## 1. Core CDK Concepts

### Q1: What is AWS CDK, and how does it differ from CloudFormation?
**Answer:**
- **AWS CDK (Cloud Development Kit)** is an open-source software development framework to define cloud infrastructure in code (IaC) using familiar programming languages (Python, TypeScript, Java, etc.).
- **Difference:** While CloudFormation uses static JSON/YAML templates, CDK allows you to use logic (if-statements, loops), object-oriented principles, and abstraction. CDK eventually **synthesizes** your code into a CloudFormation template.

### Q2: Explain the hierarchy of CDK: App, Stack, and Construct.
**Answer:**
- **Constructs:** The basic building blocks. They represent a "cloud component" (e.g., an S3 bucket or a VPC).
- **Stacks:** A unit of deployment. All resources in a stack are provisioned as a single unit (mapping 1:1 to a CloudFormation stack).
- **App:** The root container. An App can contain one or more Stacks.

### Q3: What are the different levels of Constructs (L1, L2, L3)?
**Answer:**
- **L1 (Cfn Resources):** Low-level resources that match CloudFormation resources exactly (e.g., `CfnBucket`). You must specify all properties.
- **L2 (Higher-level):** Opinionated constructs developed by AWS that come with sensible defaults, boilerplate code, and helper methods (e.g., `s3.Bucket`).
- **L3 (Patterns):** High-level patterns designed to help you complete common tasks (e.g., `ApplicationLoadBalancedFargateService`).

---

## 2. CDK Lifecycle & Commands

### Q4: What does `cdk bootstrap` do?
**Answer:**
It prepares your AWS environment (account/region) for CDK deployment. It creates a "bootstrap stack" containing an S3 bucket for file assets and IAM roles required for the deployment process.

### Q5: Explain `cdk synth` vs `cdk deploy`.
**Answer:**
- **`cdk synth`**: Synthesizes the CDK code into a CloudFormation template (outputs to `cdk.out`). It's a great way to verify the resulting template without actually deploying.
- **`cdk deploy`**: Actually provisions the resources in AWS by submitting the synthesized template to CloudFormation.

---

## 3. Practical Implementation (EC2 & VPC)

### Q6: How does CDK handle VPC creation compared to manual CloudFormation?
**Answer:**
In manual CloudFormation, you'd have to define the VPC, multiple subnets, Route Tables, Internet Gateways, and associations individually (hundreds of lines). In CDK, `ec2.Vpc(self, "MyVpc")` creates a best-practice VPC with public/private subnets across multiple AZs automatically.

### Q7: What is "User Data" in the context of an EC2 instance in CDK?
**Answer:**
User data is a script that runs when the instance launches for the first time. In CDK, we use `ec2.UserData.for_linux()` and `add_commands()` to automate software installation (like the Apache server we set up in our demo).

---

## 4. Best Practices & Security

### Q8: How do you handle secrets (API keys, passwords) in CDK?
**Answer:**
Never hardcode secrets. Use **AWS Secrets Manager** or **Systems Manager (SSM) Parameter Store**. In CDK, you can reference these using `SecretValue.secrets_manager('my-secret-id')`.

### Q9: What is the "Principle of Least Privilege" and how does CDK help?
**Answer:**
It's the practice of giving only the minimum permissions required. CDK L2 constructs often have `.grantRead()` or `.grantWrite()` methods that automatically create the smallest possible IAM policy for you.

---

## 5. Advanced Topics

### Q10: What are "Context" and "Environment" in CDK?
**Answer:**
- **Environment:** Specifies the AWS Account and Region (`env=cdk.Environment(account='...', region='...')`).
- **Context:** Key-value pairs associated with an app or stack. Used for configuration that stays the same across different environments (e.g., an ID of a pre-existing VPC).

### Q11: How do you handle cross-stack references?
**Answer:**
When one stack needs a resource from another, you pass the resource object as a property to the second stack's constructor. CDK automatically creates `Fn::ImportValue` or similar mechanisms under the hood.

### Q12: How do you test your CDK infrastructure?
**Answer:**
You can use standard testing frameworks (like `pytest` for Python). CDK provides an `assertions` module to verify that the synthesized CloudFormation template contains the expected resources and properties.

---

## 6. CI/CD for CDK

### Q13: What is "CDK Pipelines"?
**Answer:**
CDK Pipelines is a high-level construct library that makes it easy to set up continuous delivery pipelines with **AWS CodePipeline**. Its standout feature is **self-mutation**: the pipeline automatically updates its own structure when you change the pipeline definition in your code.

### Q14: Compare GitHub Actions vs. AWS CodePipeline for CDK.
**Answer:**
- **GitHub Actions**: Preferred for better Developer Experience (DX), faster feedback loops, and being where the code lives. It requires OIDC for secure AWS authentication.
- **AWS CodePipeline**: Preferred for enterprise-grade security, native IAM integration, and the self-mutation capability of CDK Pipelines. Ideal for multi-account/multi-region deployments.

### Q15: How do you handle cross-account deployments in a pipeline?
**Answer:**
Using CDK Pipelines, you define **Stages**. Each Stage can be targeted to a specific `Environment` (Account + Region). CDK handles the complex cross-account IAM role assumptions and KMS key encryption needed for the deployment artifacts automatically.

### Q16: Can you use CodeDeploy to deploy AWS CDK infrastructure?
**Answer:**
Technically, you use **AWS CloudFormation** to deploy CDK-defined infrastructure. **CodeDeploy** is typically used for the *application code* (the software running on the servers), while **CodeBuild** is used to run the CDK CLI commands (`cdk synth`, `cdk deploy`). In a standard "CDK Pipeline," CodeBuild acts as the worker that invokes CloudFormation.

---

## 💡 Top Tips for the Interview

1.  **Emphasize Reusability:** Talk about how you can create your own "Custom Constructs" to share standard infrastructure patterns across your team.
2.  **Infrastructure as Code (IaC) Mindset:** Focus on how CDK improves developer velocity because developers can use the same language for both app code and infrastructure.
3.  **Synthesize often:** Mention that you always run `cdk synth` to inspect the underlying CloudFormation before deploying to production.
4.  **Security First:** Always mention Security Groups, Private Subnets, and IAM roles when discussing EC2.
