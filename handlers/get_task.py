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
        path_parameters = event.get('pathParameters') or {}
        task_id = path_parameters.get('id')
        
        if not task_id:
            return {
                "statusCode": 400,
                "headers": HEADERS,
                "body": json.dumps({"error": "Missing task ID in path"})
            }
            
        response = table.get_item(Key={'taskId': task_id})
        item = response.get('Item')
        
        if not item:
            return {
                "statusCode": 404,
                "headers": HEADERS,
                "body": json.dumps({"error": f"Task with ID {task_id} not found"})
            }
            
        return {
            "statusCode": 200,
            "headers": HEADERS,
            "body": json.dumps({"data": item})
        }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": HEADERS,
            "body": json.dumps({"error": str(e)})
        }
