import json
import datetime
import urllib.request
import boto3

# User vars
AWS_BUCKET_NAME = 'YOUR-AWS-BUCKET'
UPLOAD_LOCATION = 'PATH/TO/DIRECTORY'
OUTPUT_FILE_LOCATION = '/tmp/'
OUTPUT_FILE_NAME = 'YOUR-FILE-NAME-HERE'

def lambda_handler(event, context):
    
    # Extract coin data from coingecko api
    apiCoinGecko = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1&sparkline=false&price_change_percentage=1h'
    req = urllib.request.Request(apiCoinGecko)
    req.add_header('accept', 'application/json')
    response = urllib.request.urlopen(req)
    res_body = response.read()
    data = json.loads(res_body.decode("utf-8"))
    with open(OUTPUT_FILE_LOCATION + OUTPUT_FILE_NAME + '.json', 'w') as f:
        f.write(json.dumps(data))
    
    
    # Upload json file to aws bucket
    dtStart = datetime.datetime.utcnow().strftime('%Y%m%d%H%M')
    s3 = boto3.client('s3')
    with open(OUTPUT_FILE_LOCATION + OUTPUT_FILE_NAME + '.json', 'rb') as f:
        s3.upload_fileobj(f, AWS_BUCKET_NAME, UPLOAD_LOCATION + OUTPUT_FILE_NAME + dtStart + '.json')
    
    return {
        'statusCode': 200,
        'body': json.dumps('All Good')
    }
