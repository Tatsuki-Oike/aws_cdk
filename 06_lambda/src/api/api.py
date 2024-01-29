import json

def hello_world(event, context):

    try:
        response = {
            "status": "SUCCESS",
            "msg": "Hello, World",
        }
        status_code = 200
    except Exception as e:
        response = {
            "ERROR": str(e)
        }
        status_code = 500
    return {
        'statusCode': status_code,
        'body': json.dumps(response)
    }