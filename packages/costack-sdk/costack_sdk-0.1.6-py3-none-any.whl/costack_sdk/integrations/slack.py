# the purpose of the function is to use costack sdk to send a slack message 
import sys
# Enable debug logging
import logging
from slack_sdk import WebClient

# we can build countless integrators 
logging.basicConfig(level=logging.DEBUG)

# then maybe we just need a secret manager 
# this may be a great idea 
slack_token = os.environ["SLACK_BOT_TOKEN"]
client = WebClient(token=slack_token)


client = WebClient()
api_response = client.api_test()
