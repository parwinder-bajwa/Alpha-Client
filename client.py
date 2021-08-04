import boto3
import os
import pandas as pd

#authentication 
session = boto3.Session(profile_name='default')
client = boto3.client('s3')

#function to check file in the bucket is exist or not
def checkBucketFile(bucket, prefix):
    exist = client.list_objects(Bucket=bucket, Prefix=prefix)
    result = ('Contents' in exist)
    return result

#function to download file from the bucket
def downloadFile(bucket, filename, key):
    client.download_file(bucket,filename,key)

#function to upload file from the bucket
def uploadFile(filename, bucket, key):
    client.upload_file(filename, bucket, key)

#function to create the file if not exist
def makeFile(hostname, attempt, filename):
    with open(filename, "w") as writer:
        string = f"{hostname},{attempt}\n"
        writer.write("hostname,attempt\n")
        writer.write(string)

#function to update the file with the latest attempt value
def modifyFile(hostname, attempt, filename):
    df = pd.read_csv(filename)
    status = False
    for ind in df.index:
        if df['hostname'][ind] == str(hostname):
            df.loc[ind,'attempt'] = str(attempt)
            df.to_csv(filename, index=False)
            status = True
            break
    if(status == False):    
        with open(filename, "a") as writer:
            string = f"{hostname},{attempt}\n"
            writer.write(string)

#function to get number of attempt from file
def checkAttempt(hostname, filename):
    df = pd.read_csv(str(filename))
    for ind in df.index:
        if df['hostname'][ind] == hostname:
            attempt = df['attempt'][ind]
            return attempt

#function to run the whole process
def job(hostname, attempt, bucket, filename):
    if checkBucketFile(bucket, filename):
        downloadFile(bucket, filename, filename)
        attempt_from_s3 = checkAttempt(hostname, filename)
        if attempt_from_s3 !=  attempt:
            modifyFile(hostname, attempt, filename)
            uploadFile(filename, bucket, filename)
    else: 
        makeFile(hostname, attempt, filename)
        uploadFile(filename, bucket, filename)


#variables that requires
myhost = os.uname()[1] #get machine hostname
bucket_name = 'your-bucket-name'
filename = 'attempt.csv'

#this total ssh attempt that failed from file ('/var/log/authlog'), fully tested on Ubuntu 18.04
#if this file doesn't exist on your end, you may check where the auth log located. 
with open('/var/log/auth.log', "r") as infile:
    content = infile.read()


total_attempt = content.count('Connection closed by authenticating')

if __name__ == "__main__":
    job(myhost, total_attempt, bucket_name, filename)









