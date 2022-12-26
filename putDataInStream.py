import json
import boto3
import csv
import datetime
import random
from getData import getData
import datetime
import warnings
warnings.filterwarnings("ignore")

kdsname='input-stream'
region='us-east-1'
i=0
clientkinesis = boto3.client('kinesis',region_name=region)

# define date range in string
start = datetime.datetime.strptime("2021-10-01", "%Y-%m-%d")
end = datetime.datetime.strptime("2021-10-31", "%Y-%m-%d")
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
dates= [date.strftime("%Y-%m-%d") for date in date_generated]

# extract GHCND data for Maryland between the dates 10-01-2022 and 10-31-2022
for date in dates:
	# get data from API in MD for a specific date.
	streamData = getData(date)
	
	# for each record in streamData corresponding to a specific date, put it in input-stream
	for data in streamData:
		response=clientkinesis.put_record(StreamName=kdsname, Data=json.dumps(data)
		, PartitionKey=date)
		print("Total ingested:"+str(len(streamData)) +",ReqID:"+ 
		response['ResponseMetadata']['RequestId']+ ",HTTPStatusCode:"+ 
		str(response['ResponseMetadata']['HTTPStatusCode']))
