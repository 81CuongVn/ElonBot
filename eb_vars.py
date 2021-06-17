import discord

help_msg = discord.Embed(title = "ELONBOT COMMANDS", description = """
    Use "eb stalk [Twitter Handle]" to select a Twitter account to get tweets from.

Use **"eb stalking"** check which Twitter account is currently being monitored.

Use **"eb addkey [keyword]"** to add a keyword to look for in account's tweets.

Use **"eb delkey [keyword]"** to remove a keyword.

Use **"eb check"** to manually tell ElonBot to check for new tweets.

Use **"eb start"** to make ElonBot start searching

Use **"eb stop"** to stop ElonBot from updating.

Use **"eb clearkey"** to clear the keywords listed.

Happy Stalking 😉
""")

#$stalk messages
def feedbackStalkNoKey(uName):
  msgStalkNoKey = f"""Okay, will notify you of tweets from **{uName}**.
  *Note: Use $addkey command to add keywords to look out for*"""
  em_msgStalkNoKey = discord.Embed(description = msgStalkNoKey)
  return em_msgStalkNoKey

def feedbackStalkHasKey(uName):
  msgStalkHasKey = f"Okay, will notify you of tweets from *{uName}*"
  em_msgStalkHasKey = discord.Embed(description = msgStalkHasKey)
  return em_msgStalkHasKey

#$addkey messages
def feedbackAddKeyExists(keyword):
  msgAddKeyExists = f"Keyword *{keyword}* already in keywords."
  em_msgAddKeyExists = discord.Embed(description = msgAddKeyExists)
  return em_msgAddKeyExists

def feedbackAddKeyNew(keyword):
  msgAddKeyNew = f"Keyword *{keyword}* added to keywords."
  em_msgAddKeyNew = discord.Embed(description = msgAddKeyNew)
  return em_msgAddKeyNew

#$delkey messages
def feedbackDelKeyExists(keyword):
  msgDelkeyExists = f"Keyword *{keyword}* removed"
  em_msgDelKeyExists = discord.Embed(description = msgDelkeyExists)
  return em_msgDelKeyExists

def feedbackDelKeyNone(keyword):
  msgDelkeyNone = f"Keyword *{keyword}* is not in your list of keywords."
  em_msgDelKeyNone = discord.Embed(description = msgDelkeyNone)
  return em_msgDelKeyNone

#$viewkey messages
msgviewkeyNone = """You haven't entered any keywords yet
*Note: Use **eb addkey** command to add keywords to look out for*"""
em_msgviewkeyNone = discord.Embed(description = msgviewkeyNone)

def feedbackViewKeyHas(desc):
  em_msgViewkeyHas = discord.Embed(description = desc)
  return em_msgViewkeyHas

#clearkey messages
em_clearKeys = discord.Embed(description = "*Keywords cleared!*")

#Relevant Tweets feedback
def feedbackNewRelTwt(uname):
  msgNewRelTwt = f"{uname} has a new tweet you might find interesting!"
  em_msgNewRelTwt = discord.Embed(description = msgNewRelTwt)
  return em_msgNewRelTwt

msgRelTweetsURL = "https://twitter.com/{}/status/{}"

def feedbackNoRelTwt(uname):
  msgNoRelTwt = f"{uname} has no new relevant tweets."
  em_msgNoRelTwt = discord.Embed(description = msgNoRelTwt)
  return em_msgNoRelTwt

#Missed Required Fields
em_setUpReqd = discord.Embed(description = """❗ATTENTION❗
Use *eb stalk <Twitter handle>* first!""")

em_keywordsReqd = discord.Embed(description = """❗ATTENTION❗
Use *eb addkey <keyword>* to set up your keywords!""")

#Monitoring feedback
def feedbackStart(uname):
  msgStart = f"Now monitoring {uname}'s tweets"
  em_msgStart = discord.Embed(description = msgStart)
  return em_msgStart

def feedbackStop(uname):
  msgStop = f"Will stop notifying you about {uname}'s tweets"
  em_msgStop = discord.Embed(description = msgStop)
  return em_msgStop

def feedbackStalking(uname):
  msgStart = f"Currently monitoring {uname}'s tweets"
  em_msgStart = discord.Embed(description = msgStart)
  return em_msgStart

keywords = []