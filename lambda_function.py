import boto3
import json
import logging
import os

from base64 import b64decode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


logger = logging.getLogger()
logger.setLevel(logging.INFO)
cloudwatch = boto3.client('cloudwatch')

# A lambda that takes an SNS event
# then publishes cool playlist metrics
# with respect to each type of API call.
def lambda_handler(event, context):
    
    ##### Extracting message
    logger.info("Event: " + str(event))
    message = json.loads(event['Records'][0]['Sns']['Message'])
    logger.info("Message: " + str(message))
    
    ##### Message parsing
    logger.info("Trying to parse message for request...")
    try:
        type_of_request = message['request_type']
        first_letter_of_playlist = message['name'][0]
        last_letter_of_playlist = message['name'][-1]
        length_of_playlist = len(message['name'])
        first_num_of_id = message['id'][0]
        last_num_of_id = message['id'][-1]
        metric_data = [
            {
                'MetricName': type_of_request + " Request",
                'Dimensions': [
                    {
                        'Name': 'First letter of playlist name',
                        'Value': first_letter_of_playlist
                    },
                    {
                        'Name': 'Last letter of playlist name',
                        'Value': last_letter_of_playlist
                    },
                    {
                        'Name': 'Length of playlist name',
                        'Value': str(length_of_playlist)
                    },
                    {
                        'Name': 'First number of playlist id',
                        'Value': str(first_num_of_id)
                    },
                    {
                        'Name': 'Last number of playlist id',
                        'Value': str(last_num_of_id)
                    }
                    ],
                    'Unit': 'Count',
                    'Value': 1
            }
        ]
        namespace = 'ProPlaylistPlaylistMetrics'
        logger.info("Message parse success.")
    except Exception as ex:
        logger.error("Could not parse the message.")
        logger.error(str(ex))
    
    ##### Metric publishing
    logger.info("Attempting to publish metric...")
    try:
        response = cloudwatch.put_metric_data(MetricData = metric_data, Namespace = namespace)
        logger.info("Metric publish success.")
    except Exception as ex:
        logger.error("Trying to publish the metric failed.")
        logger.error(str(ex))
        
