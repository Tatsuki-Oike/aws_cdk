from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
)
import aws_cdk as cdk
from constructs import Construct

class Ec2Stack(Stack):

    def __init__(self, scope: Construct,
                 name: str, region: str, ami_id: str, key_name: str, 
                 **kwargs) -> None:
        super().__init__(scope, name, **kwargs)

        # VPCの作成
        vpc = ec2.Vpc(
            self, "VPC",
            max_azs=1,
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                )
            ],
            nat_gateways=0,
        )

        # セキュリティグループの作成
        sg = ec2.SecurityGroup(
            self, "Ec2Sg",
            vpc=vpc,
            allow_all_outbound=True,
        )
        sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(22),
        )
        sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(80),
        )

        # 初期コマンド作成
        user_data = ec2.UserData.for_linux()
        html_tag = "<html><body><h1>Hello World!</h1></body></html>"
        user_data.add_commands(
            "sudo yum install -y nginx",
            "sudo systemctl start nginx",
            "sudo systemctl enable nginx",
            f'echo "{html_tag}" > /usr/share/nginx/html/index.html',
        )

        # EC2インスタンスの作成
        host = ec2.Instance(
            self, "Ec2Instance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.generic_linux(ami_map={ region: ami_id }),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            security_group=sg,
            key_pair=ec2.KeyPair.from_key_pair_name(self, "MyKeyPair", key_name),
            user_data=user_data
        )

        # パブリックIPアドレスを出力
        cdk.CfnOutput(self, "InstancePublicIp", value=host.instance_public_ip)

app = cdk.App()
Ec2Stack(
    app, "Ec2Stack",
    region="ap-northeast-1",
    ami_id="ami-05a03e6058638183d",
    key_name=app.node.try_get_context("key_name"),
)
app.synth()