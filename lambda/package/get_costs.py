import boto3
import json
from datetime import datetime, timedelta
from decimal import Decimal

def lambda_handler(event, context):
    """
    Returns last 30 days of AWS costs as JSON
    """
    
    print("📊 Fetching cost data...")
    
    # Connect to DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('aws-daily-costs')
    
    try:
        # Scan the table to get all items
        response = table.scan()
        items = response['Items']
        
        # Sort by date
        items_sorted = sorted(items, key=lambda x: x['date'])
        
        # Extract dates and costs into separate lists
        dates = []
        costs = []
        
        for item in items_sorted:
            dates.append(item['date'])
            # Convert string to float for the chart
            costs.append(float(item['cost']))
        
        # Calculate statistics
        total = sum(costs)
        average = total / len(costs) if costs else 0
        
        # Prepare response data
        data = {
            'dates': dates,
            'costs': costs,
            'total': round(total, 2),
            'average': round(average, 4),
            'count': len(costs)
        }
        
        print(f"✅ Returning {len(costs)} days of data")
        
        # Return with CORS headers so your website can call this
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET'
            },
            'body': json.dumps(data)
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }

# Test locally
if __name__ == '__main__':
    result = lambda_handler({}, {})
    print(result)