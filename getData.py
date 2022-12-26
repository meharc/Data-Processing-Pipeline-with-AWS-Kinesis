# import libraries
import requests
import json
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

####################################################################################

# the function performs the following operations:
# 1. extract date, drop unnecessary columns and add station name the data from API.
# 2. filter data for 4 values— precipitation, snowfall, minimum and maximum temperature.
# 3. create 4 dataframes for each of the 4 values and outer join them, two at a time.
def processData(parse_data,stationDict):

    # create dataframe
    intermediateDF = pd.DataFrame(parse_data['results'])

    # clean the dataframe
    # extract date from datetime column
    intermediateDF['date'] = pd.to_datetime(intermediateDF['date']).dt.date.astype('str')
    # drop attributes column
    intermediateDF=intermediateDF.drop(columns = 'attributes')
    # add station name using the station id and dictionary.
    intermediateDF['station_name'] =intermediateDF['station'].map(stationDict) 
    intermediateDF['station_name'] = intermediateDF['station_name'].apply(lambda x: x.split(',')[0]) # remove MD, USA

    # filtering data for only precipitaion, snowfall, minimum and maximum temperture
    filteredDF = intermediateDF.loc[intermediateDF['datatype'].isin(['PRCP', 'SNOW','TMAX', 'TMIN'])]

    # creating 4 dataframes to store 4 datatypes
    dataPRCP = filteredDF.loc[filteredDF['datatype']=='PRCP']
    dataSNOW = filteredDF.loc[filteredDF['datatype']=='SNOW']
    dataTMIN = filteredDF.loc[filteredDF['datatype']=='TMIN']
    dataTMAX = filteredDF.loc[filteredDF['datatype']=='TMAX']
    # rename value column as the corresponding datatype value and then drop the datatype column.
    dataPRCP.rename(columns = {'value':dataPRCP['datatype'].unique()[0]}, inplace = True)
    dataPRCP.pop("datatype")
    dataSNOW.rename(columns = {'value':dataSNOW['datatype'].unique()[0]}, inplace = True)
    dataSNOW.pop("datatype")
    dataTMIN.rename(columns = {'value':dataTMIN['datatype'].unique()[0]}, inplace = True)
    dataTMIN.pop("datatype")
    dataTMAX.rename(columns = {'value':dataTMAX['datatype'].unique()[0]}, inplace = True)
    dataTMAX.pop("datatype")

    # merge the dataframes, two at a time using full join
    merge1 = pd.merge(dataPRCP,dataSNOW,on=['date', 'station', 'station_name'],how='outer')
    merge2 = pd.merge(merge1,dataTMIN,on=['date', 'station', 'station_name'],how='outer')
    dateResult = pd.merge(merge2,dataTMAX,on=['date', 'station', 'station_name'],how='outer')
    dateResult = dateResult[['date', 'station', 'station_name', 'PRCP', 'SNOW','TMIN', 'TMAX']]

    return dateResult

# function to get all stations in MD and return a mapping of station id and and station name.
def getStationsMD():

    # define the url
    stationDict = dict()
    url = "https://www.ncei.noaa.gov/cdo-web/api/v2/stations?locationid=FIPS:24&limit=1000"

    # define parameters
    payload={}
    headers = {
    'token': 'NXcgoBGhCYiHQBNedkAxWcrTWYydxzpI'
    }

    # get response and data
    response = requests.request("GET", url, headers=headers, data=payload)
    stations = response.text

    # parse the data into JSON format.
    parse_stations= json.loads(stations)

    # add sttaion id and station name as key-value pair to the dictionary
    for station in parse_stations['results']:
        if station['id'] not in stationDict:
            stationDict[station['id']] = station['name']

    return stationDict


# main driver function to extract data for a given date, clean it and put it on stream.
def getData(date):

    # 1. Get station names in MD
    stationDict = getStationsMD()
    # There are total 938 weather stations available in MD 

    ####################################################################################

    # 2. Get GHCND data (PRCP, SNOW, TMIN, TMAX) for MD starting for the given date
    # For every date, the number of records in MD across all stations is less than 1000.
    limit = 1000

    # we can only fetch 1000 records at a time. We will get data in batches (day-wise)
    url = "https://www.ncei.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&locationid=FIPS:24&startdate="+date+"&enddate="+date+"&sortfield=date&limit="+str(limit)

    # define parameters
    payload={}
    headers = {
    'token': 'NXcgoBGhCYiHQBNedkAxWcrTWYydxzpI'
    }

    # get response and data
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.text

    # parse the data into JSON format.
    parse_data= json.loads(data)
    total_records = parse_data['metadata']['resultset']['count']

    streamData = processData(parse_data=parse_data, stationDict=stationDict)
    print('Data received for date {} with {} records.'.format(date, streamData.shape[0]))

    # convert dataframe into array of object
    streamData = streamData.to_dict('records')

    return streamData




