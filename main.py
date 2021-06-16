from eb_vars import *
import keyHandling
import csv
import tweepy
import os
import requests
import json
import eb_commands
from discord.ext import commands

consumer_token = os.environ['eb_tw_consumer']
consumer_secret = os.environ['eb_tw_csecret']
access_token = os.environ['eb_tw_access']
access_token_secret = os.environ['eb_tw_asecret']

auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twApi = tweepy.API(auth)

#ebClient = discord.Client()
cmdClient = commands.Bot(command_prefix="$")
eb_userName = ''

#discord py vars
eb_key = os.environ['ebTOKEN']


@cmdClient.event  #
async def on_ready():
    print('Logged in as {0.user}'.format(cmdClient))

@cmdClient.command()
async def poop(ctx):
    await ctx.send(help_msg)

@cmdClient.command()
async def stalk(ctx):
    msgSplit = ctx.message.content.rsplit(' ')
    handle = msgSplit[1]
    #try:
    eb_user = eb_commands.setUser(api=twApi, userString=handle, guildID=str(ctx.guild.id))
    eb_userName = eb_user.name
    if (len(eb_commands.getKeywords(guildID=str(ctx.guild.id))) == 0):
        await ctx.message.channel.send(msgStalkNoKey.format(eb_userName))
        keyHandling.createKeywordFile(str(ctx.guild.id))
    else:
        await ctx.message.channel.send(msgStalkHasKey.format(eb_userName))
        keyHandling.createKeywordFile(str(ctx.guild.id))
    #except:
    #    await ctx.message.channel.send('Sorry, that account cannot be found.')

@cmdClient.command()
async def addkey(ctx):
    msgSplit = ctx.message.content.rsplit(' ')
    keyword = msgSplit[1]
    if  eb_commands.getKeywords(guildID=str(ctx.guild.id)) != 404:
        if (keyword in eb_commands.getKeywords(guildID=str(ctx.guild.id))):
            await ctx.message.channel.send(msgAddKeyExists.format(keyword))
        else:
            eb_commands.addKeyword(keyword, guildID=str(ctx.guild.id))
            await ctx.message.channel.send(msgAddKeyNew.format(keyword))
    else:
        await ctx.send("Please use *$stalk <twitter handle>* first to set up")

@cmdClient.command()
async def delkey(ctx):
    msgSplit = ctx.message.content.rsplit(' ')
    keyword = msgSplit[1]
    keywords = eb_commands.getKeywords(guildID=str(ctx.guild.id))
    if keywords != 404:
        if keyword not in keywords:
            await ctx.message.channel.send(msgDelkeyNone.format(keyword))
        else:
            eb_commands.delKeyword(keyword, guildID=str(ctx.guild.id))
            await ctx.message.channel.send("Keyword *" + keyword + "* removed.")
    else:
        await ctx.send("Please use *$stalk <twitter handle>* first to set up")

@cmdClient.command()
async def viewkey(ctx):
    if eb_commands.getKeywords(guildID=str(ctx.guild.id)) != 404:
        if (len(eb_commands.getKeywords(guildID=str(ctx.guild.id))) == 0):
            await ctx.message.channel.send(msgviewkeyNone)
        else:
            sOut = "Your current keywords are: \n"
            for x in eb_commands.getKeywords(guildID=str(ctx.guild.id)):
                sOut = sOut + "\t*- " + x + "*\n"
            await ctx.message.channel.send(sOut)
    else:
        await ctx.send("Please use *$stalk <twitter handle>* first to set up")

@cmdClient.command()
async def clearkey(ctx):
    if eb_commands.clearKeys(guildID=str(ctx.guild.id)) != 404:
        await ctx.message.channel.send('*Keywords cleared!*')
    else:
        await ctx.send("Please use *$stalk <twitter handle>* first to set up")

@cmdClient.command()
async def check(ctx):
    if eb_commands.getUser(guildID=str(ctx.guild.id)) != 404:
        print(eb_commands.getUser(guildID=str(ctx.guild.id)))
        eb_user = eb_commands.setUser(api=twApi, userString=eb_commands.getUser(guildID=str(ctx.guild.id)), guildID=str(ctx.guild.id))
        relTweetsIds = eb_commands.getRelevantTweets(twApi, eb_user, guildID=str(ctx.guild.id))
        print(relTweetsIds)
        if len(relTweetsIds) != 0:
            for id in relTweetsIds:
                await ctx.message.channel.send(msgRelTweetsHas.format(eb_user.name, eb_commands.getUser(guildID=str(ctx.guild.id)), id))
        else:
            await ctx.message.channel.send(eb_user.name + " has no new relevant tweets")
    else:
        await ctx.send("Please use *$stalk <twitter handle>* first to set up")

@cmdClient.command()
async def reset(ctx):
    with open(str(ctx.guild.id)+'_lastIDs.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerows([[]])

#if message.content.startswith('$shutup'):
#await message.channel.send()

#TODO: main Loop
#@tasks.loop(minutes = 5)
#async def twtCheck():
#try:
# print(eb_commands.getUser(guildID=str(ctx.guild.id)))
# eb_user = eb_commands.setUser(api=twApi, userString=eb_commands.getUser(guildID=str(ctx.guild.id)), guildID=str(ctx.guild.id))
# relTweetsIds = eb_commands.getRelevantTweets(twApi, eb_user, guildID=str(ctx.guild.id))
# print(relTweetsIds)
# if len(relTweetsIds) != 0:
#   for id in relTweetsIds:
#     await ctx.message.channel.send(msgRelTweetsHas.format(eb_user.name, eb_commands.getUser(guildID=str(ctx.guild.id)), id))
# else:
#   await ctx.message.channel.send(eb_user.name + " has no new relevant tweets")
#except:
# pass

cmdClient.run(eb_key)