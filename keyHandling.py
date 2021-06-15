import os
import json

def createKeywordFile(guildID):
    if os.path.exists(str(guildID)+"_keywords.json"):
        print(guildID+"_keywords.json exists")
    else:
        with open(str(guildID)+'_keywords.json', 'x', encoding='utf-8') as file:
            initData = {
                'guildID':str(guildID),
                'user':'elonmusk',
                'keywords':[]
            }
            json.dump(initData,file)

def getKeywords(guildID):
    if os.path.exists(str(guildID)+"_keywords.json"):
        with open(str(guildID)+"_keywords.json", 'r', encoding="utf-8") as file:
            data = json.load(file)
            return data["keywords"]
    else:
        print(guildID+"_keywords.json does not exist")
        return 404

def getUser(guildID):
    if os.path.exists(str(guildID)+"_keywords.json"):
        with open(str(guildID)+"_keywords.json", 'r', encoding="utf-8") as file:
            data = json.load(file)
            return data["user"]
    else:
        print(guildID+"_keywords.json does not exist")
        return 404

def updateUser(guildID, userInput):
    if os.path.exists(str(guildID)+"_keywords.json"):
        data = {}
        with open(str(guildID)+"_keywords.json", 'r', encoding="utf-8") as file:
            data = json.load(file)
            data["user"] = userInput
        with open(str(guildID)+"_keywords.json", 'w', encoding="utf-8") as file:
            data = json.dump(data,file)
    else:
        print(str(guildID)+"_keywords.json does not exist")
        return 404

def updatekeywords(guildID, keywordList):
    if os.path.exists(str(guildID)+"_keywords.json"):
        data = {}
        with open(str(guildID)+"_keywords.json", 'r', encoding="utf-8") as file:
            data = json.load(file)
            data["keywords"] = keywordList
        with open(str(guildID)+"_keywords.json", 'w', encoding="utf-8") as file:
            data = json.dump(data,file)
    else:
        print(str(guildID)+"_keywords.json does not exist")
        return 404