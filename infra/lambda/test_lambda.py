import json
import pytest
from moto import mock_aws
import boto3

# Import inside tests to ensure fresh module state
def reload_lambda_module():
    import sys
    if 'lambda_function' in sys.modules:
        del sys.modules['lambda_function']
    from lambda_function import lambda_handler, table as lambda_table, dynamodb as lambda_dynamodb
    return lambda_handler, lambda_table, lambda_dynamodb

@mock_aws
def test_valid_request():
    # Setup mock DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.create_table(
        TableName='PageCounts',
        KeySchema=[{'AttributeName': 'pageName', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'pageName', 'AttributeType': 'S'}],
        BillingMode='PAY_PER_REQUEST'
    )
    
    # Inject mock table into Lambda module
    lambda_handler, _, _ = reload_lambda_module()
    from lambda_function import dynamodb as lambda_dynamodb, table as lambda_table
    lambda_table = table
    
    # Test valid request
    event = {'body': json.dumps({'page': 'test.html'})}
    response = lambda_handler(event, None)
    assert response['count'] == 1
    
    # Test increment
    response = lambda_handler(event, None)
    assert response['count'] == 2

@mock_aws
def test_default_page():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.create_table(
        TableName='PageCounts',
        KeySchema=[{'AttributeName': 'pageName', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'pageName', 'AttributeType': 'S'}],
        BillingMode='PAY_PER_REQUEST'
    )
    
    lambda_handler, _, _ = reload_lambda_module()
    from lambda_function import table as lambda_table
    lambda_table = table
    
    event = {'body': json.dumps({})}
    response = lambda_handler(event, None)
    assert response['count'] == 1

@mock_aws
def test_invalid_page_type():
    lambda_handler, _, _ = reload_lambda_module()
    
    event = {'body': json.dumps({'page': 123})}
    response = lambda_handler(event, None)
    assert response == {"message": "Invalid page name"}

@mock_aws
def test_long_page_name():
    lambda_handler, _, _ = reload_lambda_module()
    
    long_name = 'a' * 256
    event = {'body': json.dumps({'page': long_name})}
    response = lambda_handler(event, None)
    assert response == {"message": "Invalid page name"}

@mock_aws
def test_missing_body():
    lambda_handler, _, _ = reload_lambda_module()
    
    event = {}
    response = lambda_handler(event, None)
    assert response == {"message": "Invalid request body"}

@mock_aws
def test_invalid_json_body():
    lambda_handler, _, _ = reload_lambda_module()
    
    event = {'body': 'invalid json'}
    response = lambda_handler(event, None)
    assert response == {"message": "Invalid request body"}

@mock_aws
def test_unexpected_error():
    # Don't create table to force an error
    lambda_handler, _, _ = reload_lambda_module()
    
    event = {'body': json.dumps({'page': 'test.html'})}
    response = lambda_handler(event, None)
    assert 'message' in response
    assert 'Unexpected error' in response['message']