# How to Connect Your Environment to AWS

To deploy CDK code, your computer needs permission to talk to your AWS account. Follow these steps to set up your connection.

## 1. Install the AWS CLI
If you haven't already, install the AWS Command Line Interface (CLI).

- **Windows**: [Download the MSI Installer](https://awscli.amazonaws.com/AWSCLIV2.msi)
- **Verify installation**: Open PowerShell and type `aws --version`

## 2. Get Your Credentials
You need an **Access Key ID** and a **Secret Access Key**.

1. Log in to the **AWS Management Console**.
2. Go to **IAM** (Identity and Access Management).
3. Click on **Users** and select your username (or create a new one with `AdministratorAccess`).
4. Select the **Security credentials** tab.
5. Click **Create access key** and choose "Command Line Interface (CLI)".
6. **IMPORTANT**: Download the `.csv` file. You will not be able to see the secret key again!

## 3. Configure the CLI
Open your terminal (PowerShell or CMD) and run:

```powershell
aws configure
```

You will be prompted for four pieces of information:
1. **AWS Access Key ID**: Paste your key.
2. **AWS Secret Access Key**: Paste your secret key.
3. **Default region name**: e.g., `us-east-1` (choose the region closest to you).
4. **Default output format**: `json`

## 4. Verify the Connection
Run this command to see if AWS recognizes you:

```powershell
aws sts get-caller-identity
```

If successful, you will see your **Account ID** and **UserID** in the output.

---

## 🔐 Alternative: AWS IAM Identity Center (Recommended)
If your company uses SSO, use this instead:

```powershell
aws configure sso
```
Follow the browser prompts to log in. This is more secure as it uses temporary credentials.

---

## 💡 Troubleshooting
- **"Command not found"**: Restart your terminal after installing the AWS CLI.
- **"Invalid credentials"**: Double-check for extra spaces when pasting your keys.
- **"Time offset error"**: Ensure your computer's clock is synced and accurate.

Once connected, you can run:
```bash
cdk bootstrap
cdk deploy
```
