# AWS CDK EC2 Instance Demo

This project demonstrates how to create an EC2 instance using AWS CDK with Python.

## Architecture

This CDK stack creates:
- **VPC** with public and private subnets across 2 availability zones
- **Internet Gateway** for public subnet internet access
- **Security Group** allowing SSH (port 22), HTTP (port 80), and HTTPS (port 443)
- **EC2 Instance** (t3.micro - free tier eligible) running Amazon Linux 2023
- **Apache Web Server** automatically installed via user data script

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **AWS CLI** installed and configured
3. **Python 3.7+** installed
4. **Node.js** (for AWS CDK CLI)
5. **AWS CDK** installed globally

## Setup Instructions

### 1. Install AWS CDK CLI (if not already installed)

```bash
npm install -g aws-cdk
```

### 2. Create Python Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 4. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure AWS Credentials

Make sure your AWS credentials are configured:

```bash
aws configure
```

### 6. Bootstrap CDK (First time only)

```bash
cdk bootstrap
```

## Deployment

### 1. Synthesize CloudFormation Template

```bash
cdk synth
```

### 2. Deploy the Stack

```bash
cdk deploy
```

You'll be prompted to approve security changes. Type `y` to proceed.

### 3. View Outputs

After deployment, you'll see outputs including:
- Instance ID
- Public IP Address
- Public DNS Name
- Website URL
- SSH Command

## Accessing Your Instance

### Via Web Browser

Open the Website URL from the outputs in your browser:
```
http://<instance-public-dns>
```

You should see a welcome page served by Apache.

### Via SSH

**Note:** By default, AWS CDK doesn't create a key pair. You have two options:

**Option 1: Use EC2 Instance Connect (Recommended for testing)**
```bash
aws ec2-instance-connect send-ssh-public-key \
    --instance-id <instance-id> \
    --instance-os-user ec2-user \
    --ssh-public-key file://~/.ssh/id_rsa.pub
```

**Option 2: Add a key pair to the stack**
Modify `ec2_stack.py` to include:
```python
key_pair = ec2.KeyPair(self, "KeyPair",
    key_pair_name="ec2-demo-key"
)

instance = ec2.Instance(
    # ... other parameters ...
    key_pair=key_pair
)
```

Then SSH using:
```bash
ssh -i <your-key.pem> ec2-user@<instance-public-ip>
```

## Cost Considerations

- **t3.micro** instance is free tier eligible (750 hours/month for 12 months)
- **VPC** and **Internet Gateway** are free
- **Data transfer** charges may apply
- **No NAT Gateway** configured to save costs

## Customization Options

### Change Instance Type

In `ec2_stack.py`, modify:
```python
instance_type=ec2.InstanceType.of(
    ec2.InstanceClass.T3,
    ec2.InstanceSize.SMALL  # Change to SMALL, MEDIUM, etc.
)
```

### Add NAT Gateway (for private subnet internet access)

In `ec2_stack.py`, change:
```python
nat_gateways=1  # Change from 0 to 1
```

### Restrict SSH Access

In `ec2_stack.py`, change:
```python
security_group.add_ingress_rule(
    peer=ec2.Peer.ipv4("YOUR_IP_ADDRESS/32"),  # Replace with your IP
    connection=ec2.Port.tcp(22),
    description="Allow SSH access from my IP only"
)
```

### Use Different AMI

```python
# Ubuntu
ami = ec2.MachineImage.from_ssm_parameter(
    "/aws/service/canonical/ubuntu/server/22.04/stable/current/amd64/hvm/ebs-gp2/ami-id"
)

# Windows Server
ami = ec2.MachineImage.latest_windows(
    ec2.WindowsVersion.WINDOWS_SERVER_2022_ENGLISH_FULL_BASE
)
```

## Clean Up

To avoid ongoing charges, destroy the stack:

```bash
cdk destroy
```

Type `y` to confirm deletion.

## Useful CDK Commands

- `cdk ls` - List all stacks in the app
- `cdk synth` - Synthesize CloudFormation template
- `cdk deploy` - Deploy stack to AWS
- `cdk diff` - Compare deployed stack with current state
- `cdk destroy` - Remove stack from AWS
- `cdk doctor` - Check CDK environment

## Troubleshooting

### Issue: "Unable to resolve AWS account"
**Solution:** Ensure AWS credentials are configured: `aws configure`

### Issue: "CDK bootstrap required"
**Solution:** Run `cdk bootstrap` in your AWS account/region

### Issue: "Cannot connect via SSH"
**Solution:** 
1. Check security group allows SSH from your IP
2. Ensure you have the correct key pair
3. Use EC2 Instance Connect as an alternative

### Issue: "Website not loading"
**Solution:**
1. Wait a few minutes for user data script to complete
2. Check security group allows HTTP (port 80)
3. Verify instance is in a public subnet with Internet Gateway

## Next Steps

Consider extending this project with:
- **Auto Scaling Group** for high availability
- **Application Load Balancer** for distributing traffic
- **CloudWatch Alarms** for monitoring
- **Systems Manager** for secure access without SSH keys
- **Elastic IP** for a static IP address
- **RDS Database** for data persistence
- **S3 Bucket** for file storage

## Resources

- [AWS CDK Documentation](https://docs.aws.amazon.com/cdk/)
- [AWS CDK Python Reference](https://docs.aws.amazon.com/cdk/api/v2/python/)
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
