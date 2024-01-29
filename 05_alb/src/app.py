from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_autoscaling as autoscaling,
    aws_elasticloadbalancingv2 as elbv2,
)
import aws_cdk as cdk
from constructs import Construct

class ALBStack(Stack):

    def __init__(self, scope: Construct, 
                 name: str, region: str, ami_id: str, 
                 **kwargs) -> None:
        super().__init__(scope, name, **kwargs)

        # VPCの作成
        vpc = ec2.Vpc(
            self, "VPC",
            max_azs=2,
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

        # EC2で実行するコマンド
        user_data = ec2.UserData.for_linux()
        html_tag = "<html><body><h1>Hello World!</h1></body></html>"
        user_data.add_commands(
            "sudo yum install -y nginx",
            "sudo systemctl start nginx",
            "sudo systemctl enable nginx",
            f'echo "{html_tag}" > /usr/share/nginx/html/index.html',
        )

        # Auto Scaling
        asg = autoscaling.AutoScalingGroup(self, "MyWebAppASG",
            vpc=vpc,
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.generic_linux(ami_map={ region: ami_id }),
            min_capacity=2,
            max_capacity=3,
            security_group=sg,
            user_data=user_data,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
        )

        # ALBの作成
        alb = elbv2.ApplicationLoadBalancer(self, "MyALB",
            vpc=vpc,
            internet_facing=True
        )
        # ALBのリスナーの設定
        listener = alb.add_listener("MyListener",
            port=80
        )
        # ターゲットグループ
        target_group = elbv2.ApplicationTargetGroup(self, "MyTargetGroup",
            port=80,
            targets=[asg],
            vpc=vpc
        )
        # ターゲットグループをリスナーに関連付ける
        listener.add_target_groups("MyTargetGroups", target_groups=[target_group])
        
        # ALBのDNSNameを出力
        cdk.CfnOutput(self, "ALBDNSName", value=alb.load_balancer_dns_name)

app = cdk.App()
ALBStack(
    app, "ALBStack",
    region="ap-northeast-1",
    ami_id="ami-05a03e6058638183d",
)
app.synth()