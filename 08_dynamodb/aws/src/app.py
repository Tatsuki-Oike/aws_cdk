from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_dynamodb as dynamodb,
)
import aws_cdk as cdk
from constructs import Construct

class DynamodbStack(Stack):

    def __init__(self, scope: Construct, 
                 name: str, 
                 **kwargs) -> None:
        super().__init__(scope, name, **kwargs)

        # DynamoDBのテーブル作成
        table = dynamodb.Table(
            self, "ItemTable",
            partition_key=dynamodb.Attribute(
                name="user_id", 
                type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )

        # Lambda関数作成
        get_lambda = _lambda.Function(
            self, "GetLambda",
            code=_lambda.Code.from_asset("api"),
            handler="api.get_lambda",
            memory_size=256,
            timeout=cdk.Duration.seconds(10),
            runtime=_lambda.Runtime.PYTHON_3_9,
            environment={
                "TABLE_NAME": table.table_name
            }
        )

        post_lambda = _lambda.Function(
            self, "PostLambda",
            code=_lambda.Code.from_asset("api"),
            handler="api.post_lambda",
            memory_size=256,
            timeout=cdk.Duration.seconds(10),
            runtime=_lambda.Runtime.PYTHON_3_9,
            environment={
                "TABLE_NAME": table.table_name
            }
        )

        patch_lambda = _lambda.Function(
            self, "PatchLambda",
            code=_lambda.Code.from_asset("api"),
            handler="api.patch_lambda",
            memory_size=256,
            timeout=cdk.Duration.seconds(10),
            runtime=_lambda.Runtime.PYTHON_3_9,
            environment={
                "TABLE_NAME": table.table_name
            }
        )

        delete_lambda = _lambda.Function(
            self, "DeleteLambda",
            code=_lambda.Code.from_asset("api"),
            handler="api.delete_lambda",
            memory_size=256,
            timeout=cdk.Duration.seconds(10),
            runtime=_lambda.Runtime.PYTHON_3_9,
            environment={
                "TABLE_NAME": table.table_name
            }
        )

        # Lambda関数にテーブルを操作できる権限を付与
        table.grant_read_data(get_lambda)
        table.grant_read_write_data(post_lambda)
        table.grant_read_write_data(patch_lambda)
        table.grant_read_write_data(delete_lambda)

        # API Gatewayの作成
        api = apigw.RestApi(
            self, "ItemApi",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS,
            )
        )
        
        # API GatewayとLambda関数の連携
        api.root.add_method(
            "GET",
            apigw.LambdaIntegration(get_lambda)
        )
        api.root.add_method(
            "POST",
            apigw.LambdaIntegration(post_lambda)
        )
        item_user_api = api.root.add_resource("{user_id}")
        item_user_api.add_method(
            "PATCH",
            apigw.LambdaIntegration(patch_lambda)
        )
        item_user_api.add_method(
            "DELETE",
            apigw.LambdaIntegration(delete_lambda)
        )

app = cdk.App()
DynamodbStack(
    app, "DynamodbStack",
)
app.synth()