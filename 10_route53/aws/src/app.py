from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_s3 as s3,
    aws_route53 as route53,
    aws_certificatemanager as acm,
    aws_route53_targets as targets,
    aws_cloudfront as cfront,
    aws_cloudfront_origins as origins,
    aws_s3_deployment as s3deploy
)
import aws_cdk as cdk
from constructs import Construct

class ServerlessStack(Stack):

    def __init__(self, scope: Construct, 
                 name: str, 
                 us_acm_arn: str, acm_arn: str, hosted_zone_id: str, domain_name: str,
                 **kwargs) -> None:
        super().__init__(scope, name, **kwargs)

        # ACM証明書とホストゾーンの指定
        us_certificate = acm.Certificate.from_certificate_arn(self, "UsCertificate", us_acm_arn)
        certificate = acm.Certificate.from_certificate_arn(self, "Certificate", acm_arn)
        my_hosted_zone = route53.HostedZone.from_hosted_zone_attributes(
            self, "MyHostedZone",
            hosted_zone_id=hosted_zone_id,
            zone_name=domain_name
        )

        # Lambda関数の作成
        hello_lambda = _lambda.Function(
            self, "HelloLambda",
            code=_lambda.Code.from_asset("api"),
            handler="api.hello_world",
            memory_size=256,
            timeout=cdk.Duration.seconds(10),
            runtime=_lambda.Runtime.PYTHON_3_9,
        )

        # API Gatewayの作成
        api = apigw.RestApi(
            self, "HelloApi",
            domain_name=apigw.DomainNameOptions(
                domain_name="api."+domain_name,
                certificate=certificate
            ),
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS,
            )
        )

        # S3のバケットの作成
        bucket = s3.Bucket(
            self, "ImageBucket",
            website_index_document="index.html",
            bucket_name="www."+domain_name,
            versioned=False, 
            block_public_access=s3.BlockPublicAccess.BLOCK_ACLS,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )
        bucket.grant_public_access()

        s3deploy.BucketDeployment(self, "DeployWebsite",
            sources=[s3deploy.Source.asset("./dist")],
            destination_bucket=bucket,
        )

        # API GatewayとLambda関数の連携
        api.root.add_method(
            "GET",
            apigw.LambdaIntegration(hello_lambda)
        )

        # CloudFront
        distribution = cfront.Distribution(
            self, "SiteDistribution",
            default_behavior=cfront.BehaviorOptions(
                origin=origins.S3Origin(bucket),
                viewer_protocol_policy=cfront.ViewerProtocolPolicy.HTTPS_ONLY
            ),
            certificate=us_certificate,
            domain_names=["www." + domain_name]
        )

        # レコード作成
        route53.ARecord(self, "WebAliasRecord",
            zone=my_hosted_zone,
            target=route53.RecordTarget.from_alias(targets.CloudFrontTarget(distribution)),
            record_name="www."+domain_name
        )

        route53.ARecord(self, "ApiAliasRecord",
            zone=my_hosted_zone,
            target=route53.RecordTarget.from_alias(targets.ApiGateway(api)),
            record_name="api."+domain_name
        )
    
        # 必要な情報の出力
        cdk.CfnOutput(self, "BucketUrl", value=f"s3://{bucket.bucket_name}")

app = cdk.App()
ServerlessStack(
    app, "ServerlessStack",
    us_acm_arn=app.node.try_get_context("us_acm_arn"),
    acm_arn=app.node.try_get_context("acm_arn"),
    hosted_zone_id=app.node.try_get_context("hosted_zone_id"),
    domain_name=app.node.try_get_context("domain_name"),
    env=cdk.Environment(region="ap-northeast-1")
)
app.synth()