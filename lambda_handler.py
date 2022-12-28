import base64
import json
import os
##python lib for aws import boto3
import datetime
from decimal import Decimal
import boto3

def lambda_handler(event , context ):

    try:
        my_region = os . environ ['AWS REGION']
        ##resource assigned from boto library
        dynamo_db = boto3.resource('dynamodb', region_name=my_region) ##dynamoDB t a b l e name
        table_precipitation = dynamo_db.Table('Precipitation')
        table_temperature = dynamo_db.Table ('Temperature')
        for record in event ["Records"]:
            decoded_data = base64.b64decode(record["kinesis"]["data"]).decode("utf−8")
            # this returns a string
            # replace NaN in the string with ”NaN”
            decoded_data_handle_NaN = decoded_data.replace ("NaN" , "\"NaN\"" )
            # convert json string into python object
            decoded_data_dic = json.loads(decoded_data_handle_NaN , parse_float=Decimal)
            # separate data for precipitation and temperature and store them in respective tables .
            record_precipitation = {key: decoded_data_dic[key] for key in ["date", "station", "station_name", "PRCP", "SNOW"]}
            with table_precipitation.batch_writer () as batch_writer1 :
                batch_writer1.put_item(Item=record_precipitation)
            record_temperature = { key: decoded_data_dic[key] for key in ["date", "station", "station_name","TMIN", "TMAX"]}
            with table_temperature.batch_writer () as batch_writer2 :
                batch_writer2.put_item(Item=record_temperature)
    except Exception as e:
        print('Error Caught! {}'.format(str(e)))