from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    CfnOutput,
    Tags
)
from constructs import Construct


class EC2Stack(Stack):
    """
    CDK Stack that creates an EC2 instance with VPC and security groups.
    
    This stack includes:
    - VPC with public and private subnets across 2 AZs
    - Internet Gateway for public subnet access
    - Security Group allowing SSH and HTTP access
    - EC2 instance in the public subnet
    - User data script for initial configuration
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create VPC with public and private subnets
        vpc = ec2.Vpc(
            self, "EC2-VPC",
            vpc_name="ec2-demo-vpc",
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
            max_azs=2,  # Use 2 availability zones
            nat_gateways=0,  # No NAT gateway to save costs (can be changed to 1 for private subnet internet access)
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="Private",
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                    cidr_mask=24
                )
            ]
        )

        # Create Security Group for EC2 instance
        security_group = ec2.SecurityGroup(
            self, "EC2-SecurityGroup",
            vpc=vpc,
            security_group_name="ec2-demo-sg",
            description="Security group for EC2 instance - allows SSH and HTTP",
            allow_all_outbound=True
        )

        # Allow SSH access from anywhere (in production, restrict this to your IP)
        security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(22),
            description="Allow SSH access"
        )

        # Allow HTTP access from anywhere
        security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(80),
            description="Allow HTTP access"
        )

        # Allow HTTPS access from anywhere
        security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(443),
            description="Allow HTTPS access"
        )

        # Create EC2 instance
        # Using Amazon Linux 2023 (latest generation)
        ami = ec2.MachineImage.latest_amazon_linux2023(
            cpu_type=ec2.AmazonLinuxCpuType.X86_64
        )

        # User data script to install and configure web server
        user_data = ec2.UserData.for_linux()
        user_data.add_commands(
            "#!/bin/bash",
            "# Update system packages",
            "yum update -y",
            "",
            "# Install Apache web server",
            "yum install -y httpd",
            "",
            "# Start and enable Apache",
            "systemctl start httpd",
            "systemctl enable httpd",
            "",
            "# Create a simple web page",
            "echo '<html><head><title>AWS CDK EC2 Demo</title></head>' > /var/www/html/index.html",
            "echo '<body><h1>Hello from AWS CDK!</h1>' >> /var/www/html/index.html",
            "echo '<p>This EC2 instance was created using AWS CDK with Python.</p>' >> /var/www/html/index.html",
            "echo '<p>Instance ID: ' >> /var/www/html/index.html",
            "curl -s http://169.254.169.254/latest/meta-data/instance-id >> /var/www/html/index.html",
            "echo '</p>' >> /var/www/html/index.html",
            "echo '<p>Availability Zone: ' >> /var/www/html/index.html",
            "curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone >> /var/www/html/index.html",
            "echo '</p></body></html>' >> /var/www/html/index.html"
        )

        # Create the EC2 instance
        instance = ec2.Instance(
            self, "EC2-Instance",
            instance_name="ec2-demo-instance",
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.T3,  # T3 instance class (burstable performance)
                ec2.InstanceSize.MICRO  # Micro size (free tier eligible)
            ),
            machine_image=ami,
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PUBLIC
            ),
            security_group=security_group,
            user_data=user_data,
            # Enable detailed monitoring (optional, costs extra)
            # detailed_monitoring=True,
        )

        # Add tags to resources
        Tags.of(self).add("Project", "EC2-CDK-Demo")
        Tags.of(self).add("Environment", "Development")

        # Output the instance details
        CfnOutput(
            self, "InstanceId",
            value=instance.instance_id,
            description="EC2 Instance ID"
        )

        CfnOutput(
            self, "InstancePublicIP",
            value=instance.instance_public_ip,
            description="EC2 Instance Public IP Address"
        )

        CfnOutput(
            self, "InstancePublicDNS",
            value=instance.instance_public_dns_name,
            description="EC2 Instance Public DNS Name"
        )

        CfnOutput(
            self, "WebsiteURL",
            value=f"http://{instance.instance_public_dns_name}",
            description="Website URL (Apache web server)"
        )

        CfnOutput(
            self, "SSHCommand",
            value=f"ssh -i <your-key.pem> ec2-user@{instance.instance_public_ip}",
            description="SSH command to connect to the instance"
        )
