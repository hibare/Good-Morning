import json
import logging
import requests
from decouple import config

# Configure and create a logger
logging.basicConfig(format='%(asctime)s [%(filename)s:%(funcName)s:%(lineno)d] [%(levelname)s] %(name)s: %(message)s') 
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) 

def send_notification(text):
    try:
        logger.info("Sending slack notification")
        slack_endpoint = config('SLACK_WEBHOOK')
        headers = {
                'Content-type': 'application/json',
            }
        data = dict(
            text = text,
        )
        data = json.dumps(text)

        response = requests.post(slack_endpoint, headers=headers, data=data)
        logger.info("Slack webhook response code %s, response %s", response.status_code, response.text)

        return response.status_code
    except Exception:
        logger.exception("Exception in Slack notification")

