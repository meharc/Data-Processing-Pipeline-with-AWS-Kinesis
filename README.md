# Data-Processing-Pipeline-with-AWS-Kinesis

## INTRODUCTION

The project aims to build a pipeline that acquires weather data, processes it in real-time using AWS Kinesis, and store it in a DynamoDB table. The weather data entails information about the daily measurement for precipitation (in mm), snowfall (in mm), and minimum and maximum temperature (in Fahrenheit) for Maryland, United States between October 1, 2021, and October 31, 2021.

The project workflow broadly involves acquiring data from National Oceanic and Atmospheric Administration’s (NOAA’s) REST API, inserting data into the AWS Kinesis data stream in real-time, extracting data from the stream, and importing it into DynamoDB tables. The project will be tested based on performing queries on the imported data, contained in the DynamoDB tables.


## PROCEDURE
Following the guideline presented in Figure 3, the section describes the procedure in 7 steps.

### Step 1: Extract data using NOAA’s REST API

### Step 2: Create Kinesis data stream
In this step, we will create a data stream by using the AWS Kinesis service. Simply go to Kinesis service on AWS and click on ’Create data stream’. The stream is named as input-stream and on-demand capacity mode is used. 

### Step 3: Create Producer
Now that we have our data and data stream ready, it’s time to put the data into the stream. For this purpose, we will use AWS SDK for Python— Boto3. The SDK acts as a producer that creates a low-level service to connect to AWS Kinesis and put data onto it. For the range of dates between October 1, 2021, and October 31, 2021, we extract data, serialize each Python object in streamData variable, and put it on the stream using SDK. The code is available under the script name putDataInStream.py.

### Step 4: Ingest data into the stream
We now create an Integrated Development Environment (IDE) on AWS using Cloud9 service to run scripts and use the SDK producer to put data from the NOAA’s REST API onto the Kinesis data stream called input-stream. For this purpose, we simply go to Cloud9 service on AWS and click on ’Create environment’. The environment is named as project-kinesis with default settings as t2.micros as the EC2 instance and Amazon Linux 2 as the operating system. 

### Step 5: Create DynamoDB Tables
Before extracting the data from the data stream, we create DynamoDB tables. For this purpose, we go to AWS DynamoDB service and click on ’Create table’.

### Step 6: Create IAM Role and Policy
In this step, we will create an Identity and Access Management (IAM) role for the consumer to perform the following functions:

- Provide read access from the Kinesis data stream and write to CloudWatch logs.
- Provide edit, read and write access for the DynamoDB tables.
- 
For this purpose, we associate 1 customer managed IAM policy— *LambdaFunctionPolicy.json* and 1 AWS managed IAM policies to the role. 

### Step 7: Create Consumer
In this step, we use the AWS Lambda service to create a consumer called KinesisLambdaConsumer that gets triggered when there is data on the input-stream. For this purpose, we click on the ’Create function’ tab provided under the AWS Lambda service with the following modifications (refer Figure 11):
• Python 3.9 is chosen as the programming language to write the lambda function.
• KinesisLambdaConsumerRole is associated with the function.
• All other parameters remain unchanged.
Next, we write a Python script— lambda handler.py with a function called lambda handler to give instructions to the lambda function on how to put data from the stream onto the DynamoDB tables. In the final step, we create a trigger that invokes the lambda handler whenever there is data present in the input-stream. 

## TESTING

 The following results test the workflow of the project:
- As can be seen in Figure 7 and 15, the python3 terminal prints out the total ingested data from the REST API along with an HTTP status code as 200, verifying a successful data extraction from NOAA’s website.
- Figure 16 illustrates a 100% average success rate of GetRecords operations, that is, getting data records from kinesis data stream’s shard for the input-stream. The CloudWatch metric is available in the AWS kinesis service for a particular data stream.
- Figure 17 verifies that the lambda function was triggered over a specified amount of time.The CloudWatch metric is available in the AWS Lambda service for the KinesisLambdaConsumer function.
- The output of the project involves filling up the DynamoDB tables— Precipitation and Temperature and sorting the values using station name and date as the partition and sort key, respectively. To illustrate the successful creation of table items, a query is run to obtain the weather parameters for Beltsville in chronological order, as shown in Figure 18 and Figure 19. The query is case-sensitive, hence, it is important to provide all locations in capitals.
