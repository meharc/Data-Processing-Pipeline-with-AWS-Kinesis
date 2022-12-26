# Data-Processing-Pipeline-with-AWS-Kinesis

The project aims to build a pipeline that acquires weather data, processes it in real-time using AWS Kinesis, and store it in a DynamoDB table. The weather data entails information about the daily measurement for precipitation (in mm), snowfall (in mm), and minimum and maximum temperature (in Fahrenheit) for Maryland, United States between October 1, 2021, and October 31, 2021.

The project workflow broadly involves acquiring data from National Oceanic and Atmospheric Administration’s (NOAA’s) REST API, inserting data into the AWS Kinesis data stream in real-time, extracting data from the stream, and importing it into DynamoDB tables. The project will be tested based on performing queries on the imported data, contained in the DynamoDB tables.
