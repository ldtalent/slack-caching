#!/usr/bin/python
import os
import slack
import json
client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])
print("channels_retrieve_test: \n" )
print(client.channels_list()) 
# still testing files to struct a correct model for it 
print("channel test:\n ")
client.channels_history(channel='CQNUEAH2N')
print("replies test : \n")
print(client.channels_replies(channel='CQNUEAH2N',thread_ts='1575037903.018300'))


        
