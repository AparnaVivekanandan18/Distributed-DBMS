import json
import json
import boto3
import re
import json
import collections
import os
import pandas as pd
import csv
from csv import writer

# boto3 S3 initialization
s3_client = boto3.client("s3")
import numpy as np

def lambda_handler(event, context):
    # TODO implement
    bucketname = 'sourcedatab00870639'
    # event contains all information about uploaded object
    print("Event :", event)
    # Bucket Name where file was uploaded
    sourcebucket = event['Records'][0]['s3']['bucket']['name']
    # Filename of object (with path)
    file_key_name = event['Records'][0]['s3']['object']['key']
    input_file = os.path.join(sourcebucket, file_key_name)
    # Start the function that processes the incoming data.
    bucket = bucketname
    key = file_key_name
    response = s3_client.get_object(Bucket=sourcebucket, Key=file_key_name)
    content = response['Body'].read().decode('utf-8')
    x = content.split()
    stopwords = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out',
                 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such',
                 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him',
                 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don',
                 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while',
                 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them',
                 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because',
                 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has',
                 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being',
                 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than']
    stop_words = set(stopwords)
    tokens_without_sw = [w for w in x if w not in stop_words]
    current_word = []
    next_word = []
    data_list = [['Current_Word', 'Next_Word', 'Levenshtein_distance']]


def levenshteindistance(var1, var2):
    size_x = len(var1) + 1
    size_y = len(var2) + 1
    matrix = np.zeros((size_x, size_y))
    for x in range(size_x):
        matrix[x, 0] = x
    for y in range(size_y):
        matrix[0, y] = y
    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x - 1] == seq2[y - 1]:
                matrix[x, y] = min(matrix[x - 1, y] + 1, matrix[x - 1, y - 1], matrix[x, y - 1] + 1)
            else:
                matrix[x, y] = min(matrix[x - 1, y] + 1, matrix[x - 1, y - 1] + 1, matrix[x, y - 1] + 1)
    return (matrix[size_x - 1, size_y - 1])

    for i in range(len(tokens_without_sw) - 1):
        data_list.append([tokens_without_sw[i], tokens_without_sw[i + 1],
                          levenshteindistance(tokens_without_sw[i], tokens_without_sw[i + 1])])
        print(tokens_without_sw)
        df = pd.DataFrame(data_list)
        bytes_to_write = df.to_csv(None, header=None, index=False).encode()
        file_name = "testVector.csv"

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucketname)
    key = file_name
    ans = []

    current_data = s3_client.get_object(Bucket=bucketname, Key=file_name)
    lines = csv.reader(current_data)
    for row in lines:
        ans.append(row)
    for d in data_list:
        ans.append(d)

    file_name = "trainVector.csv"
    resfile = s3.get_object(Bucket="sourcedatab00870639", Key=file_name)
    restext = resfile["Body"].read().decode('utf-8')
    updated_data = restext + "\n" + "\n".join(str(item).strip('[]') for item in words_list)
    s3.put_object(Body=updated_data, Bucket="sourcedatab00870639 ", Key=file_name)
    print(updated_data)
