import discord
import tweepy
import requests
import json
import ossaudiodev
import os
import stalkeeClass

consumer_token = os.environ('eb_tw_consumer')
consumer_secret = os.environ('eb_tw_csecret')
access_token = os.environ('eb_tw_access')
access_token_secret =os.environ('eb_tw_asecret')

auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twApi = tweepy.API(auth)

#get user input
userInput = 'pwntifexx'

#create stalkee object
stalkee = stalkeeClass.Stalkee()

#set the user using the OAuth and user input
try:
  user = stalkee.setUser(api=twApi,userString=userInput)
except:
  print("no such user")

#add keyword(s)
stalkee.addKeyword('chimp')
stalkee.addKeyword('nim')
stalkee.addKeyword('frick')

#remove keyword(s)
stalkee.delKeyword('frick')

#retrieve tweets according to inputs using OAuth, user inputs, and instance of user object (taken from setUser)
print(stalkee.getRelevantTweets(twApi,user))