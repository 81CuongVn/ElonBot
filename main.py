#0141 AM GMT+3
from eb_vars import *
import keyHandling
import csv
import tweepy
import os
import eb_commands
import discord
from discord.ext import tasks
from discord.ext import commands

consumer_token = os.environ['eb_tw_consumer']
consumer_secret = os.environ['eb_tw_csecret']
access_token = os.environ['eb_tw_access']
access_token_secret = os.environ['eb_tw_asecret']

auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twApi = tweepy.API(auth)

#ebClient = discord.Client()
cmdClient = commands.Bot(command_prefix="eb ")
eb_userName = ''
allGuilds = cmdClient.guilds
#discord py vars
eb_key = os.environ['ebTOKEN']


@cmdClient.event  #
async def on_ready():
  print('Logged in as {0.user}'.format(cmdClient))
  twtCheck.start()

@cmdClient.command()
async def stalk(ctx):
  msgSplit = ctx.message.content.rsplit(' ')
  handle = msgSplit[1]
  #try:
  eb_user = eb_commands.setUser(api=twApi, userString=handle, guildID=str(ctx.guild.id), channelID=ctx.channel.id)
  eb_userName = eb_user.name
  if (len(eb_commands.getKeywords(guildID=str(ctx.guild.id))) == 0):
      await ctx.message.channel.send(msgStalkNoKey.format(eb_userName))
      keyHandling.createKeywordFile(ctx.channel.id, str(ctx.guild.id))
  else:
      await ctx.message.channel.send(msgStalkHasKey.format(eb_userName))
      keyHandling.createKeywordFile(ctx.channel.id, str(ctx.guild.id))
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
      await ctx.send("Please use *eb stalk <twitter handle>* first to set up")

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
      await ctx.send("Please use *eb stalk <twitter handle>* first to set up")

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
      await ctx.send("Please use *eb stalk <twitter handle>* first to set up")

@cmdClient.command()
async def clearkey(ctx):
  if eb_commands.clearKeys(guildID=str(ctx.guild.id)) != 404:
      await ctx.message.channel.send('*Keywords cleared!*')
  else:
      await ctx.send("Please use *eb stalk <twitter handle>* first to set up")

@cmdClient.command()
async def check(ctx):
  if eb_commands.getUser(guildID=str(ctx.guild.id)) != 404:
      print(eb_commands.getUser(guildID=str(ctx.guild.id)))
      eb_user = eb_commands.setUser(api=twApi, userString=eb_commands.getUser(guildID=str(ctx.guild.id)), guildID=str(ctx.guild.id), channelID=ctx.channel.id)
      relTweetsIds = eb_commands.getRelevantTweets(twApi, eb_user, guildID=str(ctx.guild.id))
      print(relTweetsIds)
      if len(relTweetsIds) != 0:
          for id in relTweetsIds:
              await ctx.message.channel.send(msgRelTweetsHas.format(eb_user.name, eb_commands.getUser(guildID=str(ctx.guild.id)), id))
      else:
          await ctx.message.channel.send(eb_user.name + " has no new relevant tweets")
  else:
      await ctx.send("Please use *eb stalk <twitter handle>* first to set up")

@cmdClient.command()
async def reset(ctx):
  with open(str(ctx.guild.id)+'_lastIDs.csv', 'w') as file:
      writer = csv.writer(file)
      writer.writerows([[]])

@cmdClient.command()
async def start(ctx):
  if eb_commands.getUser(guildID=str(ctx.guild.id)) != 404:
      if len(eb_commands.getKeywords(guildID=str(ctx.guild.id))) != 0:
          userName = eb_commands.getUser(guildID=str(ctx.guild.id))
          await ctx.send(f"Now Monitoring {userName}")
          eb_commands.setIsActive(True, ctx.guild.id)
      else:
          await ctx.send("Please use *eb addkey <keyword>* to set up keywords to look for")
  else:
      await ctx.send("Please use *eb stalk <twitter handle>* first to set up")

@cmdClient.command()
async def stop(ctx):
  if eb_commands.getUser(guildID=str(ctx.guild.id)) != 404:
      userName = eb_commands.getUser(guildID=str(ctx.guild.id))
      await ctx.send(f"Now Monitoring {userName}")
      eb_commands.setIsActive(False, ctx.guild.id)
  else:
      await ctx.send("Please use *eb stalk <twitter handle>* first to set up")

@cmdClient.command()
async def stalking(ctx):
  if eb_commands.getUser(guildID=str(ctx.guild.id)) != 404:
    eb_userHandle = eb_commands.getUser(guildID=str(ctx.guild.id))
    eb_user = eb_commands.setUser(api=twApi, userString=eb_userHandle, guildID=str(ctx.guild.id), channelID=ctx.channel.id)
    await ctx.send(f"Currently Monitoring {eb_user.name}\nhttps://twitter.com/{eb_userHandle}")
  else:
      await ctx.send("Please use *eb stalk <twitter handle>* first to set up")

#if message.content.startswith('eb shutup'):
#await message.channel.send()

@tasks.loop(seconds=30)
async def twtCheck():
    print("running twtCheck")
    #Get guild and channel IDs from _keywords.json file [[<guild ID>,<channel ID>], ...]
    IDs = eb_commands.getIDs()
    print("SERVERS USING BOT:", IDs)
    for g in IDs:
        #g[0] is guildID
        #g[1] is channelID
        if (eb_commands.getIsActive(int(g[0]))):
            if eb_commands.getUser(guildID=str(g[0])) != 404:
                eb_user = eb_commands.setUser(api=twApi, userString=eb_commands.getUser(guildID=str(g[0])), guildID=str(g[0]), channelID=g[1])
                relTweetsIds = eb_commands.getRelevantTweets(twApi, eb_user, guildID=str(g[0]))
                #DEBUG print("relTweetsIds: ", relTweetsIds)
                if len(relTweetsIds) != 0:
                    for id in relTweetsIds:
                        #DEBUG print(cmdClient.get_guild(int(g[0])).name)
                        await cmdClient.get_guild(int(g[0])).get_channel(int(g[1])).send(msgRelTweetsHas.format(eb_user.name, eb_commands.getUser(guildID=str(g[0])), id))
                else:
                    await cmdClient.get_guild(int(g[0])).get_channel(int(g[1])).send(eb_user.name + " has no new relevant tweets")
            else:
                await cmdClient.get_guild(int(g[0])).get_channel(int(g[1])).send("Please use *eb stalk <twitter handle>* first to set up")


cmdClient.run(eb_key)