import json
import boto3
import os
import logging

def lambda_handler(event, context):
    
    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)
    
    try:
        
        # obtain client
        client = boto3.client('s3')
        
        # get bucket name that triggered the event
        bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
        
        # get object (file) key that on upload triggerred the event
        object_key = event["Records"][0]["s3"]["object"]["key"] # for a file, the key would end with .txt
        
        # download file from s3 and store it in /tmp/ directory with object key as file name.
        client.download_file(bucket_name, object_key, '/tmp/'+object_key) # bucket name, key name, file name
        
        # check if file was successfully downloaded in /tmp/
        #print(os.path.isfile('/tmp/' + object_key))
        
        # read downloaded text file and convert to lower
        with open('/tmp/'+object_key, 'r') as input:
            output = input.read().lower()
            
        # save the output in a new text file lowercase-object_key
        with open('/tmp/lowercase-'+object_key, 'a') as out:
            out.write(output)
    
        # upload the modified file to write bucket
        client.upload_file('/tmp/lowercase-'+object_key,'mehar-output-bucket', 'lowercase-'+object_key) # file name, bucket name, object key
        
        # remove the originial and modified files from /tmp/
        os.remove('/tmp/'+object_key)
        os.remove('/tmp/lowercase-'+object_key)
        
        # check if file was successfully downloaded in /tmp/ - should be False
        #print(os.path.isfile('/tmp/' + object_key))
        
    except Exception as e:
        raise logger.error(e)
