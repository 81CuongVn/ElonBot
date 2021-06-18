import csv
import os
import keyHandling
import tweepy
import json

def getUser(guildID):
    #DEBUG print("getUser method called")
    return keyHandling.getUser(guildID)

def getKeywords(guildID):
    keywords = keyHandling.getKeywords(guildID)
    if keywords != 404:
        #DEBUG print("getKeywords method called")
        return keywords
    else:
        return 404

#setUser method [REQUIRED]
def setUser(api, userString, guildID, channelID):
    keyHandling.createKeywordFile(channelID, guildID)
    keyHandling.updateUser(guildID, userString)
    user = api.get_user(userString)
    print(user.location)
    print(user.description)
    return user


#addKeyword function
def addKeyword(keyword, guildID):
    keywords = keyHandling.getKeywords(guildID)
    if keywords == 404:
        return keywords
    else:
        keywords.append(keyword)
        keyHandling.updatekeywords(guildID,keywordList=keywords)
        #DEBUG print(keywords)

#delKeyword function
def delKeyword(keyword, guildID):
    keywords = keyHandling.getKeywords(guildID)
    try:
        keywords.remove(keyword)
        keyHandling.updatekeywords(guildID,keywordList=keywords)
        #DEBUG print(keywords)
    except:
        print("no such keyword")
        
#clearKeywords function
def clearKeys(guildID):
    keywords = keyHandling.getKeywords(guildID)
    if keywords != 404:
        keywords.clear()
        keyHandling.updatekeywords(guildID,keywordList=keywords)
        return 0
    else:
        return 404

#getRelevantTweets function
def getRelevantTweets(api, userInstance, guildID):
    recentTweets_id = []
    lastUserTweet_dic = {}
    relevantTweetIDs = []
    
    if os.path.exists(f"./guild-files/{guildID}_lastIDs.csv"):
        print(guildID+"_lastIDs.csv exists")
    else:
        open(f"./guild-files/{guildID}_lastIDs.csv", 'x', encoding='utf-8')


    #import most recent tweet id of user
    try:
        with open(f"./guild-files/{guildID}_lastIDs.csv", 'r', encoding='utf-8') as lastIDs:
            reader = csv.reader(lastIDs)
            lastUserTweet_dic = {rows[0]:rows[1] for rows in reader}
    except:
        print('error csv')
    print(lastUserTweet_dic)

    userHandle = getUser(guildID)
    keywords = getKeywords(guildID)

    #If the user does not exist in the csv file, create a new dictionary key
    if userHandle not in lastUserTweet_dic:
        lastUserTweet_dic[userHandle] = '0'

    #Using tweepy Cursor, get the max 10 most recent tweets' IDs including last most recent tweet
    #IDs stored in recentTweets_id
    for status in tweepy.Cursor(api.user_timeline, id=userInstance.id).items(10):
        if int(status.id) > int(lastUserTweet_dic[userHandle]):
            recentTweets_id.append([status.id])

    #for each ID, check to see if the tweet contains the keyword/s. if it does, add into list of relevant tweets 
    for id in recentTweets_id:
        status = api.get_status(id[0], tweet_mode="extended")
        try:                    # Retweet
            for word in keywords:
                if word in status.retweeted_status.full_text:
                    relevantTweetIDs.append(id[0])
                    #print("[RETWEET] ", status.retweeted_status.full_text)
        except AttributeError:  # Not a Retweet
            for word in keywords:
                if word in status.full_text:
                    relevantTweetIDs.append(id[0])
                    #print(status.full_text)

    #check to see if recentTweets_id is empty. if so, skip updating csv file and return empty list
    if len(recentTweets_id) == 0:
      return recentTweets_id

    #export recent tweet of user to csv file
    if userHandle in lastUserTweet_dic:    #update an existing user's most recent tweet id
        lastUserTweet_dic[userHandle] = recentTweets_id[0][0]
        with open(f"./guild-files/{guildID}_lastIDs.csv", 'w', encoding='utf-8', newline='') as lastIDs:
            writer = csv.writer(lastIDs)
            for key in lastUserTweet_dic.keys():
                lastIDs.write("%s,%s\n"%(key,lastUserTweet_dic[key]))
    else:                                 #append new user's most recent tweet id
        with open(f"./guild-files/{guildID}_lastIDs.csv", 'a', encoding='utf-8', newline='') as lastIDs:
            writer = csv.writer(lastIDs)
            writer.writerows([[userHandle,recentTweets_id[0][0]]])

    #remove duplicate tweet IDs
    finalTweetIDS = []
    for i in relevantTweetIDs:
        if i not in finalTweetIDS:
            finalTweetIDS.append(i)
    return finalTweetIDS

#Make a list of guildIDs and channelIDs from json files
def getIDs():
    IDs = []
    for file in os.listdir("./guild-files/"):
        print("FILE:", file)
        if file.endswith(".json") and not file.startswith("101_keywords"): #101_keywords.json is a test file
            with open(file, 'r') as jsonFile:
                print("opened:",file)
                jsonData = json.load(jsonFile)
                guildID = jsonData["guildID"]
                channelID = jsonData["activeChannelID"]
                IDs.append([guildID, channelID])
    return(IDs)

#Check guild start/stop setting
def getIsActive(guildID):
    with open(f"./guild-files/{guildID}_keywords.json", 'r') as jsonFile:
        jsonData = json.load(jsonFile)
        #DEBUG print(jsonData)
        setting = jsonData["is_active"]
        return setting

#update guild start/stop setting
def setIsActive(newSetting,guildID):
    jsonData = []
    with open(f"./guild-files/{guildID}_keywords.json", 'r') as jsonFile:
        jsonData = json.load(jsonFile)

    jsonData["is_active"] = newSetting
    with open(f"./guild-files/{guildID}_keywords.json", 'w') as jsonFile:
        json.dump(jsonData, jsonFile)