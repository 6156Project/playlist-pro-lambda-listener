
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
# then publishes cool username metrics
# with respect to each type of API call.
def lambda_handler(event, context):
    
    ##### Extracting message
    logger.info("Event: " + str(event))
    message = json.loads(event['Records'][0]['Sns']['Message'])
    logger.info("Message: " + str(message))
    
    ##### Message parsing
    logger.info("Trying to parse message for request...")
    try:
        type_of_request = message['request_type'] # TODO: this should be GET, POST, PATCH, etc.
        first_letter_of_username = message['username'][0] # TODO: probably the user's email, we may need to some parsing there
        last_letter_of_username = message['username'][-1]
        length_of_username = len(message['username'])
        metric_data = [
            {
                'MetricName': type_of_request + " Request",
                'Dimensions': [
                    {
                        'Name': 'First letter of username',
                        'Value': first_letter_of_username
                    },
                    {
                        'Name': 'Last letter of username',
                        'Value': last_letter_of_username
                    },
                    {
                        'Name': 'Length of username',
                        'Value': str(length_of_username)
                    }
                    ],
                    'Unit': 'Count',
                    'Value': 1
            }
        ]
        namespace = 'ProPlaylistUsernameMetrics'
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
        
