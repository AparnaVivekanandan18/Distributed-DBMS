import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    s3=boto3.client('sns')
    data=json.loads(event['Records'][0]['body'])
    print(data)
    data=str(data)
    response = s3.publish(
    TopicArn='arn:aws:sns:us-east-1:513581466480:b00870639topic',
    Message=data,
    Subject='string',
    MessageStructure='string',
    MessageAttributes={
        'string': {
            'DataType': 'string',
            'StringValue': 'string',
            'BinaryValue': b'bytes'
        }
    },
    MessageDeduplicationId = 'string',
    MessageGroupId = "string"

    )
