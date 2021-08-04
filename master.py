
from flask import Flask
import boto3
import pandas as pd
from io import StringIO

#run via web console
app = Flask(__name__)

#authentication
session = boto3.Session(profile_name='default')
client = session.client('s3')

#variables that required
bucket_name = 'your-bucket-name'
object_key = 'attempt.csv'

#function to check bucket file is exist or not
def checkBucketFile(bucket, prefix):
    exist = client.list_objects(Bucket=bucket, Prefix=prefix)
    result = ('Contents' in exist)
    return result

#function to read from file in S3
@app.route("/")  # this sets the route to this page
def read():
    string = ""

    if checkBucketFile(bucket_name, object_key):
        csv_obj = client.get_object(Bucket=bucket_name, Key=object_key)
        body = csv_obj['Body']
        csv_string = body.read().decode('utf-8')
        df = pd.read_csv(StringIO(csv_string))

        for ind in df.index:
            item =  (f"{df['hostname'][ind]} had {df['attempt'][ind]} attempt<br/>")
            string += item

    else:
        string = '<h1>No data available</h1>'
    
    return string
        
if __name__ == "__main__":
    app.run()