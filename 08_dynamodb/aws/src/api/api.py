import traceback
import json
import boto3
import os

db = boto3.resource("dynamodb")
table = db.Table(os.environ["TABLE_NAME"])

HEADERS = {
    "Access-Control-Allow-Origin": "*",
}

def get_lambda(event, context):

    try:
        table_items = table.scan()
        items = table_items.get("Items")
        while table_items.get("LastEvaluateKey"):
            table_items = table.scan(ExclusiveStartKey=table_items["LastEvaluatedKey"])
            items.extend(table_items["Items"])
            
        response = {
            "status": "SUCCESS",
            "contents": str(items),
        }
        status_code = 200
    except Exception as e:
        response = {
            "status": "ERROR",
            "headers": HEADERS,
            "contents": {
                "errorMsg": str(e),
                "detail": traceback.format_exc()
            }
        }
        status_code = 500
    return {
        'statusCode': status_code,
        'body': json.dumps(response)
    }

def post_lambda(event, context):

    try:

        body = event.get('body')
        body = json.loads(body)

        db_resp = table.put_item(
                Item=body
                )
        
        response = {
            "status": "SUCCESS",
            "contents": db_resp
        }
        status_code = 200
    except Exception as e:
        response = {
            "status": "ERROR",
            "contents": {
                "errorMsg": str(e),
                "detail": traceback.format_exc()
            }
        }
        status_code = 500
    return {
        'statusCode': status_code,
        "headers": HEADERS,
        'body': json.dumps(response)
    }

def patch_lambda(event, context):

    try:

        path_params = event.get('pathParameters')
        user_id = path_params.get("user_id")

        body = event.get('body')
        body = json.loads(body)

        db_resp = table.update_item(
            Key={"user_id": user_id},
            UpdateExpression="SET #items = :value",
            ExpressionAttributeNames={
                "#items": "items",
            },
            ExpressionAttributeValues={
                ":value": body,
            }
        )
        
        response = {
            "status": "SUCCESS",
            "headers": HEADERS,
            "contents": db_resp
        }
        status_code = 200
    except Exception as e:
        response = {
            "status": "ERROR",
            "contents": {
                "errorMsg": str(e),
                "detail": traceback.format_exc()
            }
        }
        status_code = 500
    return {
        'statusCode': status_code,
        "headers": HEADERS,
        'body': json.dumps(response)
    }

def delete_lambda(event, context):

    try:

        path_params = event.get('pathParameters')
        user_id = path_params.get("user_id")

        db_resp = table.delete_item(
            Key={"user_id": user_id},
        )
        
        response = {
            "status": "SUCCESS",
            "contents": db_resp
        }
        status_code = 200
    except Exception as e:
        response = {
            "status": "ERROR",
            "contents": {
                "errorMsg": str(e),
                "detail": traceback.format_exc()
            }
        }
        status_code = 500
    return {
        'statusCode': status_code,
        "headers": HEADERS,
        'body': json.dumps(response)
    }