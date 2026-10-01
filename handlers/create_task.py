import json
import uuid
import os
import boto3
from datetime import datetime

# Connection pooling outside the handler for container reuse
dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TASKS_TABLE']
table = dynamodb.Table(table_name)

HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
}

def handler(event, context):
    try:
        body = json.loads(event.get('body') or '{}')
        
        # Validation
        if not body.get('title'):
            return {
                "statusCode": 400,
                "headers": HEADERS,
                "body": json.dumps({"error": "Title is required"})
            }
            
        task_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat() + "Z"
        
        item = {
            'taskId': task_id,
            'title': body['title'],
            'description': body.get('description', ''),
            'priority': body.get('priority', 'MEDIUM'),
            'status': body.get('status', 'PENDING'),
            'createdAt': now,
            'updatedAt': now
        }
        
        table.put_item(Item=item)
        
        return {
            "statusCode": 201,
            "headers": HEADERS,
            "body": json.dumps({
                "message": "Task created successfully",
                "data": item
            })
        }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": HEADERS,
            "body": json.dumps({"error": str(e)})
        }
