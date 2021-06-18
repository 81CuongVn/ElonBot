from eb_vars import *
import keyHandling
import csv
import tweepy
import os
import eb_commands
from keepalive import keepalive
from discord.ext import tasks, commands

consumer_token = os.environ['eb_tw_consumer']
consumer_secret = os.environ['eb_tw_csecret']
access_token = os.environ['eb_tw_access']
access_token_secret = os.environ['eb_tw_asecret']
eb_key = os.environ['ebTOKEN']
adminIDs = [243362449351376906, 691884210776047767, 427146663891697672]

auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twApi = tweepy.API(auth) #TWITTER API OBJECT

cmdClient = commands.Bot(command_prefix="eb ") #DISCORD BOT OBJECT
allGuilds = cmdClient.guilds

@cmdClient.event
async def on_ready():
  print('Logged in as {0.user}'.format(cmdClient))
  twtCheck.start()

# COMMANDS
# eb stalk <twitter handle>
#   Using the command's context (ctx), we are able to create/update a keyword.json file containing the guild's ID and that channel ID of where 
#   the command was given. When the _keyword.json file is created, the initial values (user:"elonmusk", keywords=[], is_active:"false") will be 
#   stored (this can be found in the eb_commands.setUser() function). After creating/updating the keyword file, depending on the circumstance,
#   the bot will send a message saying that you're now monitoring the user, or send a 'sorry' message saying that it cannot be found
@cmdClient.command()
async def stalk(ctx, twitterHandle):
  is_admin_only = keyHandling.isAdminOnly(str(ctx.guild.id))
  is_server_admin = ctx.author.guild_permissions.administrator
  if is_admin_only and is_server_admin or not is_admin_only:
    handle = twitterHandle
    #try:
    eb_user = eb_commands.setUser(api=twApi, userString=handle, guildID=str(ctx.guild.id), channelID=ctx.channel.id)
    eb_userName = eb_user.name
    if (len(eb_commands.getKeywords(guildID=str(ctx.guild.id))) == 0):
        await ctx.message.channel.send(embed = feedbackStalkNoKey(eb_userName))
        keyHandling.createKeywordFile(ctx.channel.id, str(ctx.guild.id))
    else:
        await ctx.message.channel.send(embed = feedbackStalkHasKey(eb_userName))
        keyHandling.createKeywordFile(ctx.channel.id, str(ctx.guild.id))
  
# eb addkey <keyword>
#   the addkey command will start by checking if a keywords.json file exists for the server. if a file does not exist, the bot will send a
#   message saying that you need to use the "eb stalk" command first. if a file does exist, the program will check if the keyword you entered
#   is already in the list of keywords. Depending on the circumstance, the bot will send a corresponding message. If the keyword does not
#   already exist in the list, then it will run the eb_commands.addKeyword() method and update the keywords.json file using the guild ID as a
#   parameter. 
@cmdClient.command()
async def addkey(ctx, key):
  is_admin_only = keyHandling.isAdminOnly(str(ctx.guild.id))
  is_server_admin = ctx.author.guild_permissions.administrator
  if is_admin_only != 404:
    if is_admin_only and is_server_admin or not is_admin_only:
      keyword = key
      #if  eb_commands.getKeywords(guildID=str(ctx.guild.id)) != 404:
      if (keyword in eb_commands.getKeywords(guildID=str(ctx.guild.id))):
          await ctx.message.channel.send(embed = feedbackAddKeyExists(keyword))
      else:
          eb_commands.addKeyword(keyword, guildID=str(ctx.guild.id))
          await ctx.message.channel.send(embed = feedbackAddKeyNew(keyword))
  else:
      await ctx.send(embed = em_setUpReqd)

# eb delkey <keyword>
#   This command works the same way as the eb addkey command. The only differnce is that it will check the keywords taken from the keywords.json
#   file and if the file exists, it will check if the keyword the user wants to delete is in the file. If it does, update the keywords.json file
#   using eb_commands.delKeyword method.
@cmdClient.command()
async def delkey(ctx, key):
  is_admin_only = keyHandling.isAdminOnly(str(ctx.guild.id))
  is_server_admin = ctx.author.guild_permissions.administrator
  if is_admin_only != 404:
    if is_admin_only and is_server_admin or not is_admin_only:
      keyword = key
      keywords = eb_commands.getKeywords(guildID=str(ctx.guild.id))
      #if keywords != 404:
      if keyword not in keywords:
          await ctx.message.channel.send(embed = feedbackDelKeyNone(keyword))
      else:
          eb_commands.delKeyword(keyword, guildID=str(ctx.guild.id))
          await ctx.message.channel.send(embed = feedbackDelKeyExists(keyword))
  else:
      await ctx.send(embed = em_setUpReqd)

# eb viewkey
#   This program will check to see if a keywords.json file exists for the server. If it doesn't, discord will send a message. If it does exist,
#   then it will check if the list is empty. Depending on the circumstance, the bot will send a corresponding message
@cmdClient.command()
async def viewkey(ctx):
  is_admin_only = keyHandling.isAdminOnly(str(ctx.guild.id))
  is_server_admin = ctx.author.guild_permissions.administrator
  if is_admin_only != 404:
    if is_admin_only and is_server_admin or not is_admin_only:
      #if eb_commands.getKeywords(guildID=str(ctx.guild.id)) != 404:
      if (len(eb_commands.getKeywords(guildID=str(ctx.guild.id))) == 0):
          await ctx.message.channel.send(embed = em_msgviewkeyNone)
      else:
          sOut = "Your current keywords are: \n"
          for x in eb_commands.getKeywords(guildID=str(ctx.guild.id)):
              sOut = sOut + "\t*- " + x + "*\n"
          await ctx.message.channel.send(embed = feedbackViewKeyHas(sOut))
  else:
      await ctx.send(embed = em_setUpReqd)

# eb clearkey
#   The program will check to see if a keywords.json file exists, if it does exist, it will proceeed to run the eb_commands.clearKeys method
#   if it doesn't, discord will send a message.
@cmdClient.command()
async def clearkey(ctx):
  is_admin_only = keyHandling.isAdminOnly(str(ctx.guild.id))
  is_server_admin = ctx.author.guild_permissions.administrator
  if is_admin_only != 404:
    if is_admin_only and is_server_admin or not is_admin_only:
      #if eb_commands.clearKeys(guildID=str(ctx.guild.id)) != 404:
      await ctx.message.channel.send(embed = em_clearKeys)
  else:
      await ctx.send(embed = em_setUpReqd)

# eb check
#   This method will first get a twitter user object using the eb_commands.setUser method using the existing values from the context.
#   (basically taking the existing info from the json file and replacing it with itself)
#   then depending on if a keywords.json file exists for the server, it will proceed to get all the relevant tweets depending on the values
#   stored in both the lastIDs.csv file and keywords.json file for the server.

#   eb_commands.getRelevantTweets
#     In getting the most relevant tweets, the program will first check if a lastIDs.csv file exists for the server. This file is for storing
#     the ID of one or more twitter users' most recent tweet. (This is taken so that the program will always be updated and only check the newest
#     tweets, and not the ones that have already been notified. The csv file will have two columns: the user's twitter handle, and their latest
#     tweet ID) If a lastIDs.csv file does not exist for the server, the program will create one.
#     After creating a lastIDs.csv file, the program will check if the twitter user exists in the file. If not, it will create a new key-value 
#     pair. [<twitter handle>, 0] (0 is the latest tweet ID since we still have yet to check the user's top 10 latest tweets.)
#     It will then check their top 10 latest tweets (or less than 10 depending if the user has not tweeted 10 more tweets since the last tweet ID 
#     that was stored in the csv) and filter out the tweets that are relevant (the tweets that contain the keyword) using a for loop and then 
#     store the relevant tweets in a list. 
#     This is where the program will update the csv file to [<twitter handle>, <latest tweet ID>] and return the list of all the latest relevant
#     tweets.

#   returning to the "eb check" command, if the list of new tweets is empty (meaning that there are no new relevant tweets), then
#   the bot will send a corresponding message. If one or more new tweets are present in the list, then the bot will send all the 
#   new tweets consecutively.
@cmdClient.command()
async def check(ctx):
  is_admin_only = keyHandling.isAdminOnly(str(ctx.guild.id))
  is_server_admin = ctx.author.guild_permissions.administrator
  if is_admin_only != 404:
    if is_admin_only and is_server_admin or not is_admin_only:
      #if eb_commands.getUser(guildID=str(ctx.guild.id)) != 404:
      print(eb_commands.getUser(guildID=str(ctx.guild.id)))
      eb_user = eb_commands.setUser(api=twApi, userString=eb_commands.getUser(guildID=str(ctx.guild.id)), guildID=str(ctx.guild.id), channelID=ctx.channel.id)
      relTweetsIds = eb_commands.getRelevantTweets(twApi, eb_user, guildID=str(ctx.guild.id))
      print(relTweetsIds)
      if len(relTweetsIds) != 0:
          for id in relTweetsIds:
              await ctx.message.channel.send(embed = feedbackNewRelTwt(eb_user.name))
              await ctx.message.channel.send(msgRelTweetsURL.format(eb_commands.getUser(guildID=str(ctx.guild.id)), id))
      else:
          await ctx.message.channel.send(embed = feedbackNoRelTwt(eb_user.name))
  else:
      await ctx.send(embed = em_setUpReqd)

# eb reset
#   This will empty out the lastIDs.csv file for the guild using the a csv writer
@cmdClient.command()
async def reset(ctx):
  is_admin_only = keyHandling.isAdminOnly(str(ctx.guild.id))
  is_server_admin = ctx.author.guild_permissions.administrator
  if is_admin_only != 404:
    if is_admin_only and is_server_admin or not is_admin_only:
      with open(f'./guild-files/{ctx.guild.id}_lastIDs.csv', 'w') as file:
          writer = csv.writer(file)
          writer.writerows([[]])
  else:
    await ctx.send(embed = em_setUpReqd)

# eb start
#   This will first check to see if a keywords.json file exists for the server. If it doesn't the bot will send a corresponding message.
#   If it does exist, it will then check if the keyword list is empty usign the eb_commands.getKeywords method, if so then the bot will send a 
#   corresponding message. If there are keywords, then the program will update the json file's is_active key to True.
@cmdClient.command()
async def start(ctx):
  is_admin_only = keyHandling.isAdminOnly(str(ctx.guild.id))
  is_server_admin = ctx.author.guild_permissions.administrator
  if is_admin_only != 404:
    if is_admin_only and is_server_admin or not is_admin_only:
      #if eb_commands.getUser(guildID=str(ctx.guild.id)) != 404:
      if len(eb_commands.getKeywords(guildID=str(ctx.guild.id))) != 0:
        userName = eb_commands.getUser(guildID=str(ctx.guild.id))
        await ctx.send(embed = feedbackStart(userName))
        eb_commands.setIsActive(True, ctx.guild.id)
      else:
        await ctx.send(embed = em_keywordsReqd)
  else:
    await ctx.send(embed = em_setUpReqd)

# eb stop
#   This will first check to see if a keywords.json file exists for the server. If it doesn't the bot will send a corresponding message.
#   If it does exist, it will then check if the keyword list is empty usign the eb_commands.getKeywords method, if so then the bot will send a 
#   corresponding message. If there are keywords, then the program will update the json file's is_active key to False using 
#   eb_commands.setIsActive.
@cmdClient.command()
async def stop(ctx):
  is_admin_only = keyHandling.isAdminOnly(str(ctx.guild.id))
  is_server_admin = ctx.author.guild_permissions.administrator
  if is_admin_only != 404:
    if is_admin_only and is_server_admin or not is_admin_only:
      #if eb_commands.getUser(guildID=str(ctx.guild.id)) != 404:
      userName = eb_commands.getUser(guildID=str(ctx.guild.id))
      await ctx.send(embed = feedbackStop(userName))
      eb_commands.setIsActive(False, ctx.guild.id)
  else:
      await ctx.send(embed = em_setUpReqd)

# eb stalking
#   This will first check to see if a keywords.json file exists for the server. If it doesn't the bot will send a corresponding message.
#   If it does exist, it will then take the userHandle from the json using eb_commands.getUser and user object using eb_commands.setUser
#   with the parameters not being updated (basically taking the existing info from the json file and replacing it with itself). 
#   The bot will then output a message including a link to the twitter user's profile.
@cmdClient.command()
async def stalking(ctx):
  is_admin_only = keyHandling.isAdminOnly(str(ctx.guild.id))
  print("is_admin_only:", str(is_admin_only))
  is_server_admin = ctx.author.guild_permissions.administrator
  print("is_server_admin:", str(is_server_admin))
  if is_admin_only != 404:
    if is_admin_only and is_server_admin or not is_admin_only:
      if eb_commands.getUser(guildID=str(ctx.guild.id)) != 404:
        eb_userHandle = eb_commands.getUser(guildID=str(ctx.guild.id))
        eb_user = eb_commands.setUser(api=twApi, userString=eb_userHandle, guildID=str(ctx.guild.id), channelID=ctx.channel.id)
        await ctx.send(embed = feedbackStalking(eb_user.name))
        await ctx.send(f"https://twitter.com/{eb_userHandle}")
      else:
          await ctx.send(embed = em_setUpReqd)

#HELP MESSAGE
cmdClient.remove_command("help")
@cmdClient.group(invoke_without_command = True)
async def help(ctx):
  await ctx.send(embed = help_msg)

#DEV/ADMIN ONLY COMMANDS
# Cog Loading and Unloading commands can only be used by developers and admins
@cmdClient.command() #DEV ONLY
async def load(ctx, extension):
  if ctx.author.id in adminIDs:
    cmdClient.load_extension(f'cogs.{extension}')
    await ctx.send(f"Loaded Cog {extension}")
  else:
    await ctx.send("You do not have permission to use this command")
  
@cmdClient.command() #DEV ONLY
async def unload(ctx, extension):
  if ctx.author.id in adminIDs:
    cmdClient.unload_extension(f'cogs.{extension}')
    await ctx.send(f"Unloaded Cog {extension}")
  else:
    await ctx.send("You do not have permission to use this command")
    
@cmdClient.event #DEV ONLY
async def on_message(message):
  if message.content.startswith("eb announce"):
    if message.author.id in adminIDs:
      IDs = eb_commands.getIDs()
      for g in IDs:
        #g[0] is guild ID
        #g(1) is channel ID
        msgList = message.content.split(" ")[2:]
        final = ""
        for word in msgList:
          final += word
          final += " "
        await cmdClient.get_guild(int(g[0])).get_channel(int(g[1])).send(final)
  await cmdClient.process_commands(message)

for file in os.listdir("./cogs"):
  if file.endswith('.py'):
    cmdClient.load_extension(f"cogs.{file[:-3]}")

#CHECK FOR NEW TWEETS EVERY X SECONDS
#   This background tasks will run for as long as the program itself is running.
#   Program will first go through a list of all the guilds the bot is active in. This is done by checking the file directory for all the
#   keyword.json files and looking at each one's guild IDs. The guild IDs will then be stored in a list.
#   For each server ID in the list, it will run the same code as the eb check command. The only difference being that since there is no
#   message context because it is not a command, it cannot find the channel of where it is supposed to send the message in each server.
#   To fix this, we store the guild ID and the active channel ID in the json file whenever we use the "eb stalk" command (check eb stalk
#   command for more details). Using the json file, we can get the channel it was called from, and use that channel ID to send the message
#   to the channel of the corresponding ID.
@tasks.loop(seconds=30)
async def twtCheck():
    print("running twtCheck")
    #Get guild and channel IDs from _keywords.json file [[<guild ID>,<channel ID>], ...]
    IDs = eb_commands.getIDs()
    print("SERVERS USING BOT:", IDs)
    for g in IDs:
        #NOTE: g[0] is guildID
        #NOTE: g[1] is channelID
        if (eb_commands.getIsActive(int(g[0]))):
            if eb_commands.getUser(guildID=str(g[0])) != 404:
                eb_user = eb_commands.setUser(api=twApi, userString=eb_commands.getUser(guildID=str(g[0])), guildID=str(g[0]), channelID=g[1])
                relTweetsIds = eb_commands.getRelevantTweets(twApi, eb_user, guildID=str(g[0]))
                #DEBUG print("relTweetsIds: ", relTweetsIds)
                if len(relTweetsIds) != 0:
                    for id in relTweetsIds:
                        #DEBUG print(cmdClient.get_guild(int(g[0])).name)
                        await cmdClient.get_guild(int(g[0])).get_channel(int(g[1])).send(embed = feedbackNewRelTwt(eb_user.name))
                        await cmdClient.get_guild(int(g[0])).get_channel(int(g[1])).send(msgRelTweetsURL.format(eb_commands.getUser(guildID=str(g[0])), id))
                else:
                  pass
                  #await cmdClient.get_guild(int(g[0])).get_channel(int(g[1])).send(embed = feedbackNoRelTwt(eb_user.name))
            else:
              await cmdClient.get_guild(int(g[0])).get_channel(int(g[1])).send(embed = em_setUpReqd)

#This will run the flask program that will be pinged every ~5 minutes
keepalive()

#This will run the Discord Bot uring the Token given.
cmdClient.run(eb_key)