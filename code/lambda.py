import json
import urllib.parse
import boto3
import csv
import requests

print('Loading function')

s3 = boto3.client('s3')

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        #print("CONTENT TYPE: " + response['ContentType'])
        #s3_files= response["Contents"]
       # print("response: "+response)
       # file_content = json.loads(s3.get_object(Bucket=bucket, Key=key)
        #print(type(response))
        #print(response['Body'].read().decode('utf-8').splitlines())
        data = response['Body'].read().decode('utf-8').splitlines()
        lines = csv.reader(data)
        headers = next(lines)
        print('headers: %s' %(headers))
        for line in lines:
         #print complete line
         #print(line)
         #print(line[0], line[1], line[2])
         
         #Store the data in the database
         # api-endpoint
         
         #Check if the record exist
         URL_GET = "https://7e8tdmhsh1.execute-api.us-east-2.amazonaws.com/items/{0}"
         headers = {"Content-Type": "application/json"}
         URL= "https://7e8tdmhsh1.execute-api.us-east-2.amazonaws.com/items"
         urlformat=URL_GET.format(line[0])
         print('urlformat: %s' %(urlformat))
         getResult=requests.get(url = urlformat).json()
         print('getResult: %s' %(getResult))
         #Asume that the value is stored, not needed of update
        # if(len(result.values())==0){
         PARAMS = {"Id":line[0], "Date":line[1], "Transaction":line[2]}
             # sending get request and saving the response as response object
         r = requests.put(url = URL, data=json.dumps(PARAMS), headers=headers)
         print(r.text)
         #}
         
         #After preserve all the info in the Database, proceed to calculate
  
        
#        print("s3_files: "+s3_files)
        
        return response['ContentType']
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

