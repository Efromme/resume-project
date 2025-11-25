import boto3
import json
from datetime import datetime
import uuid

def lambda_handler(event, context):
    """
    Logs deployment information to DynamoDB
    Called by GitHub Actions after successful deployment
    """
    
    print("📝 Logging deployment...")
    
    # Parse the deployment info from GitHub Action
    body = json.loads(event.get('body', '{}'))
    
    # Connect to DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('deployment-history')
    
    try:
        # Generate unique deployment ID
        deployment_id = str(uuid.uuid4())
        
        # Get current date and timestamp
        now = datetime.now()
        date = now.strftime('%Y-%m-%d')
        timestamp = int(now.timestamp())
        
        # Create deployment record
        item = {
            'date': date,  # Partition key
            'timestamp': timestamp,  # Sort key
            'deployment_id': deployment_id,
            'commit_message': body.get('commit_message', 'Unknown'),
            'commit_sha': body.get('commit_sha', 'Unknown')[:7],  # Short SHA
            'commit_author': body.get('commit_author', 'Unknown'),
            'branch': body.get('branch', 'main'),
            'status': 'success',
            'deployed_at': now.isoformat(),
            'commit_url': body.get('commit_url', ''),  # NEW
            'workflow_url': body.get('workflow_url', ''),  # NEW
            's3_bucket': 'resume.ethanfromme.com',
            'cloudfront_invalidation': body.get('invalidation_id', 'N/A')
        }
        
        # Save to DynamoDB
        table.put_item(Item=item)
        print(f"✅ Logged deployment: {deployment_id}")
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'message': 'Deployment logged successfully',
                'deployment_id': deployment_id,
                'date': date,
                'timestamp': timestamp
            })
        }
        
    except Exception as e:
        print(f"❌ Error logging deployment: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

# Test locally
if __name__ == '__main__':
    # Test event simulating GitHub Action
    test_event = {
        'body': json.dumps({
            'commit_message': 'Add AWS cost dashboard',
            'commit_sha': 'abc123def456',
            'commit_author': 'Ethan Fromme',
            'branch': 'main',
            'files_changed': 3,
            'invalidation_id': 'I2ABC123'
        })
    }
    result = lambda_handler(test_event, {})
    print(result)