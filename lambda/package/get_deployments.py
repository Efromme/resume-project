import boto3
import json
from decimal import Decimal
from datetime import datetime, timedelta

class DecimalEncoder(json.JSONEncoder):
    """Helper to convert Decimal to float/int for JSON"""
    def default(self, obj):
        if isinstance(obj, Decimal):
            # Convert to int if it's a whole number, otherwise float
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    """
    Returns deployment history from DynamoDB
    """
    
    print("📊 Fetching deployment history...")
    
    # Connect to DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('deployment-history')
    
    try:
        # Scan table to get all deployments
        response = table.scan()
        items = response['Items']
        
        # Sort by timestamp (newest first)
        items_sorted = sorted(items, key=lambda x: x['timestamp'], reverse=True)
        
        # Get latest 10 deployments
        recent_deployments = items_sorted[:10]
        
        # Calculate some stats
        total_deployments = len(items)
        
        # Get today's deployments
        today = datetime.now().strftime('%Y-%m-%d')
        today_deployments = [d for d in items if d.get('date') == today]
        
        print(f"✅ Returning {len(recent_deployments)} recent deployments")
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET'
            },
            'body': json.dumps({
                'deployments': recent_deployments,
                'total': total_deployments,
                'today_count': len(today_deployments)
            }, cls=DecimalEncoder)
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': 'https://resume.ethanfromme.com'
            },
            'body': json.dumps({'error': str(e)})
        }

# Test locally
if __name__ == '__main__':
    result = lambda_handler({}, {})
    print(json.dumps(json.loads(result['body']), indent=2))