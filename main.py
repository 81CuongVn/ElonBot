from eb_vars import *
from methods import *
import discord
import os
import requests
import json

ebClient = discord.Client()

#discord py vars
eb_key = os.environ['ebTOKEN']
eb_discServerId = 

@ebClient.event #
async def on_ready():
  print('Logged in as {0.user}'.format(ebClient))

@ebClient.event
async def on_message(message):

  #checks if message is from itself
  if message.author == ebClient.user:
    return
  
  if message.content.startswith('$help'):
    await message.channel.send(help_msg)

  #choose Twitter account 
  if message.content.startswith('$stalk'):
    msgSplit = message.content.rsplit(' ')
    handle = msgSplit[1]
    eb_user = handle
    #setUser(handle)
    if (len(keywords) == 0):
      await message.channel.send(msgStalkNoKey.format(handle))
    else: 
      await message.channel.send(msgStalkHasKey.format(handle))
  
  #Add Keyword
  if message.content.startswith('$addkey'):
    msgSplit = message.content.rsplit(' ')
    keyword = msgSplit[1]
    if (keyword in keywords):
      await message.channel.send(msgAddKeyExists.format(keyword))
    else:
      keywords.append(keyword)
      await message.channel.send(msgAddKeyNew.format(keyword))

  #Remove Keyword
  if message.content.startswith('$delkey'):
    msgSplit = message.content.rsplit(' ')
    keyword = msgSplit[1]
    if keyword not in keywords:
      await message.channel.send(msgDelkeyNone.format(keyword))
    else:
      keywords.remove(keyword)
      await message.channel.send("Keyword* " + keyword + "*removed.")

  if message.content.startswith('$viewkey'):
    if (len(keywords) == 0):
      await message.channel.send(msgviewkeyNone)
    else:
      sOut = "Your current keywords are: \n"
      for x in keywords:
        sOut = sOut + "\t*- " + x + "*\n"
      await message.channel.send(sOut)

  if message.content.startswith('$clearkey'):
    keywords.clear()
    await message.channel.send('*Keywords cleared!*')

  #if message.content.startswith('$shutup'):
    #await message.channel.send()

  #disc to csv


ebClient.run(eb_key)
