import os, random
import tweepy as tp
import requests

# OtterAnHour Twitter Bot
# By Nate Stutte

# https://twitter.com/OtterAnHour

def lambda_handler(event, context):
    auth = tp.OAuthHandler(os.environ['api_key'], os.environ['api_secret'])
    auth.set_access_token(os.environ['access_token'], os.environ['access_secret'])

    api = tp.API(auth)

    api.verify_credentials()
    print("Verified Credentials!")
    randompic = random.choice(os.listdir("./otterpics"))
    api.update_with_media(status="#otters", filename=f"./otterpics/{randompic}")
    print("Sent tweet!")