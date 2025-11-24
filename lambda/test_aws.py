import boto3

ce = boto3.client('ce', region_name= 'us-east-1')

print("Success! Boto3 can connect to AWS")
print(f"Using region:' {ce.meta.region_name}")