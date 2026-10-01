import json
import os
import boto3

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TASKS_TABLE']
table = dynamodb.Table(table_name)

HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
}

def handler(event, context):
    try:
        response = table.scan()
        items = response.get('Items', [])
        
        return {
            "statusCode": 200,
            "headers": HEADERS,
            "body": json.dumps({
                "count": len(items),
                "data": items
            })
        }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": HEADERS,
            "body": json.dumps({"error": str(e)})
        }
