import json
import boto3


s3 = boto3.client('s3')

def lambda_handler(event, context):

    job_id = event["job_id"]
    duration = event["duration"]

    body = json.dumps({"duration": duration + 1})

    s3.put_object(
        Body=body,
        Bucket='test-df-1977',
        Key=f'test-{job_id}.json'
    )

    return {
        'statusCode': 200,
        'body': body
    }
