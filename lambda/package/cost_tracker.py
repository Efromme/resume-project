import boto3
import json
from datetime import datetime, timedelta
from decimal import Decimal
import os

def lambda_handler(event, context):
    """
    This function runs daily to track AWS costs.
    """
    
    print("🚀 Cost Tracker starting...")
    
    # Calculate yesterday's date
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    start_date = yesterday.strftime('%Y-%m-%d')
    end_date = today.strftime('%Y-%m-%d')
    
    print(f"📅 Getting costs for: {start_date}")
    
    # Create Cost Explorer client
    ce = boto3.client('ce', region_name='us-east-1')
    
    # Call the AWS API to get costs
    try:
        response = ce.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='DAILY',
            Metrics=['UnblendedCost']
        )
        
        # Extract the cost from the response
        cost_data = response['ResultsByTime'][0]
        amount = cost_data['Total']['UnblendedCost']['Amount']
        unit = cost_data['Total']['UnblendedCost']['Unit']
        
        print(f"💰 Cost: ${amount} {unit}")
         
        # NEW: Save to DynamoDB
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('aws-daily-costs')
        
        # Prepare the item to save
        item = {
            'date': start_date,
            'cost': amount,
            'currency': unit,
            'timestamp': datetime.now().isoformat()
        }
        
        # Save it
        table.put_item(Item=item)
        print(f"💾 Saved to DynamoDB!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }

    except Exception as e:
        print(f"❌ Error getting costs: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
    
    print("✅ Cost Tracker finished!")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Success!')
    }

if __name__ == '__main__':
    lambda_handler({}, {})