from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_s3 as s3,
)
import aws_cdk as cdk
from constructs import Construct

class LambdaBucketStack(Stack):

    def __init__(self, scope: Construct, 
                 name: str, 
                 **kwargs) -> None:
        super().__init__(scope, name, **kwargs)

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
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS,
            )
        )

        # S3のバケットの作成
        bucket = s3.Bucket(
            self, "ImageBucket",
            website_index_document="index.html",
            versioned=False, 
            block_public_access=s3.BlockPublicAccess.BLOCK_ACLS,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )
        bucket.grant_public_access()

        # API GatewayとLambda関数の連携
        api.root.add_method(
            "GET",
            apigw.LambdaIntegration(hello_lambda)
        )

        # 必要な情報の出力
        cdk.CfnOutput(self, "BucketUrl", value=f"s3://{bucket.bucket_name}")
        cdk.CfnOutput(self, 'BucketWebUrl', 
                      value=f"http://{bucket.bucket_website_domain_name}")

app = cdk.App()
LambdaBucketStack(
    app, "LambdaBucketStack",
)
app.synth()