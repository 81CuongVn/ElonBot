import csv
import tweepy

class Stalkee:
    def __init__(self):
        self._userHandle = ""
        self._keywords = []

    def getUser(self):
         print("getUser method called")
         return self._userHandle

    def getKeywords(self):
         print("getKeywords method called")
         return self._keywords
    
    #setUser method [REQUIRED]
    def setUser(self, api, userString):
        self._userHandle = userString
        user = api.get_user(userString)
        print(user.location)
        print(user.description)
        return user

    #addKeyword function
    def addKeyword(self, keyword):
        self._keywords.append(keyword)
        print(self._keywords)

    #delKeyword function
    def delKeyword(self, keyword):
        try:
            self._keywords.remove(keyword)
            print(self._keywords)
        except:
            print("no such keyword")
            
    #clearKeaywords function
    def clearKeys(self):
      try:
          self._keywords.clear()
      except:
          print("Unable to clear keywords")

    #getRelevantTweets function
    def getRelevantTweets(self, api, userInstance):
        recentTweets_id = []
        lastUserTweet_dic = {}
        relevantTweetIDs = []

        #import most recent tweet id of user
        try:
            with open('lastIDs.csv', 'r', encoding='utf-8') as lastIDs:
                reader = csv.reader(lastIDs)
                lastUserTweet_dic = {rows[0]:rows[1] for rows in reader}
        except:
            print('error csv')
        print(lastUserTweet_dic)

        #If the user does not exist in the csv file, create a new dictionary key
        if self._userHandle not in lastUserTweet_dic:
            lastUserTweet_dic[self._userHandle] = '0'

        #Using tweepy Cursor, get the max 10 most recent tweets' IDs including last most recent tweet
        #IDs stored in recentTweets_id
        for status in tweepy.Cursor(api.user_timeline, id=userInstance.id).items(10):
            if int(status.id) >= int(lastUserTweet_dic[self._userHandle]):
                recentTweets_id.append([status.id])

        #for each ID, check to see if the tweet contains the keyword/s. if it does, add into list of relevant tweets 
        for id in recentTweets_id:
            status = api.get_status(id[0], tweet_mode="extended")
            try:                    # Retweet
                for word in self._keywords:
                    if word in status.retweeted_status.full_text:
                        relevantTweetIDs.append(id[0])
                        #print("[RETWEET] ", status.retweeted_status.full_text)
            except AttributeError:  # Not a Retweet
                for word in self._keywords:
                    if word in status.full_text:
                        relevantTweetIDs.append(id[0])
                        #print(status.full_text)

        #export recent tweet of user to csv file
        if self._userHandle in lastUserTweet_dic:    #update an existing user's most recent tweet id
            lastUserTweet_dic[self._userHandle] = recentTweets_id[0][0]
            with open('lastIDs.csv', 'w', encoding='utf-8', newline='') as lastIDs:
                writer = csv.writer(lastIDs)
                for key in lastUserTweet_dic.keys():
                    lastIDs.write("%s,%s\n"%(key,lastUserTweet_dic[key]))
        else:                                 #append new user's most recent tweet id
            with open('lastIDs.csv', 'a', encoding='utf-8', newline='') as lastIDs:
                writer = csv.writer(lastIDs)
                writer.writerows([[self._userHandle,recentTweets_id[0][0]]])

        #remove duplicate tweet IDs
        finalTweetIDS = []
        for i in relevantTweetIDs:
            if i not in finalTweetIDS:
                finalTweetIDS.append(i)
        return finalTweetIDS

    userHandle = property(getUser, setUser)
    keywords = property(getKeywords, addKeyword)