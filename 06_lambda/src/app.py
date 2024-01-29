from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
)
import aws_cdk as cdk
from constructs import Construct

class LambdaStack(Stack):

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

        # API GAteway作成
        api = apigw.RestApi(
            self, "HelloApi",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS,
            )
        )

        # API GatewayとLambda関数の連携
        api.root.add_method(
            "GET",
            apigw.LambdaIntegration(hello_lambda)
        )

app = cdk.App()
LambdaStack(
    app, "LambdaStack",
)
app.synth()