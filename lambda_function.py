import os, random
import tweepy as tp
import requests
import boto3
import tempfile
import json

# OtterAnHour Twitter Bot
# By Nate Stutte

# https://twitter.com/OtterAnHour

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    s3_resource = boto3.resource('s3')

    auth = tp.OAuthHandler(os.environ['api_key'], os.environ['api_secret'])
    auth.set_access_token(os.environ['access_token'], os.environ['access_secret'])

    api = tp.API(auth)

    api.verify_credentials()
    print("Verified Credentials!")

    # Load JSON file of used filenames
    content_object = s3_resource.Object("otterpics", "used.json")
    usedfilenames = json.loads(content_object.get()['Body'].read().decode('utf-8'))

    if len(usedfilenames) > 200:
        usedfilenames = []

    # ty https://stackoverflow.com/questions/59225939/get-only-file-names-from-s3-bucket-folder
    filenames = []
    result = s3_client.list_objects_v2(Bucket="otterpics")
    for item in result['Contents']:
        files = item['Key']
        filenames.append(files)   #optional if you have more filefolders to got through.

    while(1):
        img = random.choice(filenames)
        if img not in usedfilenames:
            break
    usedfilenames.append(img)
    s3_client.put_object(Body=json.dumps(usedfilenames), Bucket="otterpics", Key="used.json")

    bucket = s3_resource.Bucket("otterpics")
    img_obj = bucket.Object(img)
    
    tmp = tempfile.NamedTemporaryFile(mode='r+b')
    with open(tmp.name, 'r+b') as f:
        img_obj.download_file(tmp.name)
        print(tmp.name)
        api.update_with_media(filename=tmp.name)

    print("Sent tweet!")
