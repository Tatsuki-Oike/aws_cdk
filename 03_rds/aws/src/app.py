from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_rds as rds,
    SecretValue
)
import aws_cdk as cdk
from constructs import Construct

class Ec2RdsStack(Stack):

    def __init__(self, scope: Construct, 
                 name: str, region: str, ami_id: str, key_name: str, 
                 username: str, password: str, database_name: str,
                 **kwargs) -> None:
        super().__init__(scope, name, **kwargs)

        # VPCの作成
        vpc = ec2.Vpc(
            self, "VPC",
            max_azs=2,
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                ),
                ec2.SubnetConfiguration(
                    name="public2",
                    subnet_type=ec2.SubnetType.PUBLIC,
                ),
                ec2.SubnetConfiguration(
                    name="private",
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                ),
                ec2.SubnetConfiguration(
                    name="private2",
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                ),
            ],
            nat_gateways=0,
        )
        
        # セキュリティグループの作成
        ec2_sg = ec2.SecurityGroup(
            self, "Ec2Sg",
            vpc=vpc,
            allow_all_outbound=True,
        )
        ec2_sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(22),
        )
        ec2_sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(80),
        )

        rds_sg = ec2.SecurityGroup(
            self, "RdsSg",
            vpc=vpc,
            allow_all_outbound=True,
        )
        rds_sg.add_ingress_rule(
            peer=ec2.Peer.ipv4(vpc.vpc_cidr_block),
            connection=ec2.Port.tcp(3306),
        )
        
        # 認証情報
        credentials = rds.Credentials.from_username(
            username,
            password=SecretValue.unsafe_plain_text(password)
            )
        
        # RDSデータベースの作成
        rds_instance = rds.DatabaseInstance(
            self, "MyRDS",
            engine=rds.DatabaseInstanceEngine.maria_db(version=rds.MariaDbEngineVersion.VER_10_5),
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED), 
            security_groups=[rds_sg],
            multi_az=True,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            credentials=credentials,
            database_name=database_name
            )
        
        # 初期コマンド作成
        user_data = ec2.UserData.for_linux()
        user_data.add_commands(
            "sudo yum update -y",
            "sudo dnf install -y mariadb105-server",
            f"echo 'export MYSQL_HOST={rds_instance.db_instance_endpoint_address}' >> /etc/environment",
            f"echo 'export MYSQL_USER={username}' >> /etc/environment",
            f"echo 'export MYSQL_PASSWORD={password}' >> /etc/environment",
            f"echo 'export MYSQL_DATABASE={database_name}' >> /etc/environment",
            "source /etc/environment",
            "sudo yum install -y git",
            "git clone https://github.com/Tatsuki-Oike/aws_cdk.git",
            "cd ./aws_cdk/03_rds/flask",
            "python3 -m venv venv",
            "source venv/bin/activate",
            "python3 -m pip install --upgrade pip",
            "pip3 install -r requirements.txt",
            "sudo -E venv/bin/python app.py"
        )

        # EC2インスタンスの作成
        host = ec2.Instance(
            self, "Ec2Instance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.generic_linux(ami_map={ region: ami_id }),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            security_group=ec2_sg,
            key_pair=ec2.KeyPair.from_key_pair_name(self, "MyKeyPair", key_name),
            user_data=user_data
        )
        
        # パブリックIPアドレスを表示
        cdk.CfnOutput(self, "InstancePublicIp", value=host.instance_public_ip)

app = cdk.App()
Ec2RdsStack(
    app, "Ec2RdsStack",
    region="ap-northeast-1",
    ami_id="ami-05a03e6058638183d",
    key_name=app.node.try_get_context("key_name"),
    username=app.node.try_get_context("username"),
    password=app.node.try_get_context("password"),
    database_name=app.node.try_get_context("database_name"),
)
app.synth()