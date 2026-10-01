import json
import os
import boto3
from datetime import datetime

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
            
        body = json.loads(event.get('body') or '{}')
        now = datetime.utcnow().isoformat() + "Z"
        
        check = table.get_item(Key={'taskId': task_id})
        if 'Item' not in check:
            return {
                "statusCode": 404,
                "headers": HEADERS,
                "body": json.dumps({"error": f"Task with ID {task_id} not found"})
            }

        update_expression = "SET updatedAt = :u"
        expression_values = {":u": now}
        expression_names = {}

        if 'title' in body:
            update_expression += ", #t = :t"
            expression_values[":t"] = body['title']
            expression_names["#t"] = "title"

        if 'description' in body:
            update_expression += ", #d = :d"
            expression_values[":d"] = body['description']
            expression_names["#d"] = "description"

        if 'priority' in body:
            update_expression += ", priority = :p"
            expression_values[":p"] = body['priority']

        if 'status' in body:
            update_expression += ", #s = :s"
            expression_values[":s"] = body['status']
            expression_names["#s"] = "status"

        kwargs = {
            'Key': {'taskId': task_id},
            'UpdateExpression': update_expression,
            'ExpressionAttributeValues': expression_values,
            'ReturnValues': 'ALL_NEW'
        }
        if expression_names:
            kwargs['ExpressionAttributeNames'] = expression_names

        response = table.update_item(**kwargs)
        
        return {
            "statusCode": 200,
            "headers": HEADERS,
            "body": json.dumps({
                "message": "Task updated successfully",
                "data": response.get('Attributes')
            })
        }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": HEADERS,
            "body": json.dumps({"error": str(e)})
        }
