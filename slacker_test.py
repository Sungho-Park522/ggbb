import time
import pyupbit
import datetime
import ccxt
import pprint
import pandas as pd
import requests
 
def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )
    print(response)
 
myToken = "xoxb-2058296221329-2045897155603-ujqzc8GEWSw90Ql1uN5I14m5"
 
post_message(myToken,"#kimauto","dd")