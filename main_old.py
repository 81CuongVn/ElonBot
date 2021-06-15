from eb_vars import *
import csv
import discord
import tweepy
import os
import requests
import json
from discord.ext import commands

consumer_token = os.environ['eb_tw_consumer']
consumer_secret = os.environ['eb_tw_csecret']
access_token = os.environ['eb_tw_access']
access_token_secret = os.environ['eb_tw_asecret']

auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twApi = tweepy.API(auth)

stalkee =  1#stalkeeClass.Stalkee()

ebClient = discord.Client()
cmdClient = commands.Bot(command_prefix="1")
eb_userName = ''
eb_user = stalkee.setUser(api=twApi, userString='Twitter')

#discord py vars
eb_key = os.environ['ebTOKEN']


@ebClient.event  #
async def on_ready():
    print('Logged in as {0.user}'.format(ebClient))

@ebClient.event
async def on_message(message):

    #checks if message is from itself
    if message.author == ebClient.user:
        return

    if message.content.startswith('$help'):
        await message.channel.send(help_msg)

    #Stalk Method (choose Twitter account)
    if message.content.startswith('$stalk'):

        msgSplit = message.content.rsplit(' ')
        handle = msgSplit[1]
        #setUser(handle)
        try:
            eb_user = stalkee.setUser(api=twApi, userString=handle)
            eb_userName = eb_user.name
            if (len(stalkee.getKeywords()) == 0):
                await message.channel.send(msgStalkNoKey.format(eb_userName))
            else:
                await message.channel.send(msgStalkHasKey.format(eb_userName))
        except:
            await message.channel.send('Sorry, that account cannot be found.')

    #Add Keyword
    if message.content.startswith('$addkey'):
        msgSplit = message.content.rsplit(' ')
        keyword = msgSplit[1]
        if (keyword in stalkee.getKeywords()):
            await message.channel.send(msgAddKeyExists.format(keyword))
        else:
            stalkee.addKeyword(keyword)
            await message.channel.send(msgAddKeyNew.format(keyword))

    #Remove Keyword
    if message.content.startswith('$delkey'):
        msgSplit = message.content.rsplit(' ')
        keyword = msgSplit[1]
        if keyword not in stalkee.getKeywords():
            await message.channel.send(msgDelkeyNone.format(keyword))
        else:
            stalkee.delKeyword(keyword)
            await message.channel.send("Keyword *" + keyword + "* removed.")

    #View Keywords
    if message.content.startswith('$viewkey'):
        if (len(stalkee.getKeywords()) == 0):
            await message.channel.send(msgviewkeyNone)
        else:
            sOut = "Your current keywords are: \n"
            for x in stalkee.getKeywords():
                sOut = sOut + "\t*- " + x + "*\n"
            await message.channel.send(sOut)

    #Clear Keywords
    if message.content.startswith('$clearkey'):
        stalkee.clearKeys()
        await message.channel.send('*Keywords cleared!*')

    #Check method
    if message.content.startswith('$check'):
      print(stalkee.getUser())
      eb_user = stalkee.setUser(api=twApi, userString=stalkee.getUser())
      relTweetsIds = stalkee.getRelevantTweets(twApi, eb_user)
      print(len(relTweetsIds))
      if len(relTweetsIds) != 0:
        for id in relTweetsIds:
          await message.channel.send(msgRelTweetsHas.format(eb_user.name, stalkee.getUser(), id))
      else:
          await message.channel.send(eb_user.name + " has no new relevant tweets")

    #Reset method
    if message.content.startswith('$reset'):
        message.author.guild.id
        with open('lastIDs.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerows([[]])

    #if message.content.startswith('$shutup'):
    #await message.channel.send()

    #TODO: main Loop
    #while (len(eb_user) != 0):
      #relTweets = stalkee.getRelevantTweets(twApi, eb_user)


ebClient.run(eb_key)