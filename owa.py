from datetime import datetime
import os, uuid, json
import requests
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

# these credentials should be pulled from a secure location
AZURE_ACCOUNT_NAME='YOUR_NAME_NAME'
AZURE_API_KEY='YOUR_SECRET_KEY'

OPENWEATHERMAP_API_KEY='YOUR_SECRET_KEY'


# list of locations to get weather data
cities = [
    'beaumont',
    'bloomington',
    'chicago',
    'atlanta',
    'austin',
    'seattle'
]


def upload_data(blob):
    connect_str = "DefaultEndpointsProtocol=https;AccountName={};AccountKey={};EndpointSuffix=core.windows.net".format(AZURE_ACCOUNT_NAME, AZURE_API_KEY)

    try:
        print("Azure Blob Storage v" + __version__ + " - Python quickstart sample")

        # Create the BlobServiceClient object which will be used to create a container client
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        # use the point-in-time container
        container_name = "p-o-t"

        datetimestamp = datetime.now().strftime('%Y_%m_%d_%H_%M')

        # Create a file name to upload
        file_name = datetimestamp + "_pot.txt"

        # Create a blob client using the file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)

        print("\nUploading to Azure Storage as blob:\n\t" + file_name)

        # Upload the created file
        blob_client.upload_blob(json.dumps(blob))

    except Exception as ex:
        print('Exception:')
        print(ex)


def get_data(city):
    api_address='http://api.openweathermap.org/data/2.5/weather?appid={}&q='.format(OPENWEATHERMAP_API_KEY)

    url = api_address + city

    json_data = requests.get(url).json()

    return json_data

if __name__=='__main__':
    data = []
    for city in cities:
        data.append(get_data(city))
    upload_data(data)
