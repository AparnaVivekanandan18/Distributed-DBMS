import json
import boto3

def lambda_handler(event, context):
    print("Lambda function is calling.....")
    s3 = boto3.client("s3")
    bucket = "b00870639aparna"
    key = "tweets.txt"

    bucketContents = s3.get_object(Bucket=bucket, Key=key)
    print("bucket contents")
    print(bucketContents)

    paragraph = str(bucketContents['Body'].read())
    print("paragraph")
    print(paragraph)

    comprehend = boto3.client('comprehend')

    for i in range(0, len(paragraph.split()), 2000):
        response = comprehend.detect_sentiment(Text=paragraph[i:i + 2000], LanguageCode='en')
        print(response)
