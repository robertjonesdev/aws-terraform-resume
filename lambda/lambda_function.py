import json
import boto3

client = boto3.client('dynamodb')
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table('PageCounts')
tableName = 'PageCounts'

def lambda_handler(event, context):
    try:
        # Parse JSON body from POST request
        body = json.loads(event['body'])
        page_name = body.get('page', 'index.html')
        
        # Input validation
        if not isinstance(page_name, str) or len(page_name) > 255:
            return {"message": "Invalid page name"}
            
        # Update DynamoDB
        response = table.update_item(
            Key={'pageName': page_name},
            UpdateExpression="SET #count = if_not_exists(#count, :start) + :incr",
            ExpressionAttributeNames={'#count': 'count'},
            ExpressionAttributeValues={':incr': 1, ':start': 0},
            ReturnValues="UPDATED_NEW"
        )
        
        return {'count': response['Attributes']['count']}
        
    except (json.JSONDecodeError, KeyError):
        return {"message": "Invalid request body"}
    except Exception as e:
        return {"message": f"Unexpected error: {str(e)}"}
