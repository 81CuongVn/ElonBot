import os
import json

def createKeywordFile(channelID, guildID):
    data = {}
    if os.path.exists(f"./guild-files/{guildID}_keywords.json"):
        #Update Channel ID
        with open(f'./guild-files/{guildID}_keywords.json', 'r', encoding="utf-8") as file:
            data = json.load(file)
        data["activeChannelID"] = channelID
        with open(f'./guild-files/{guildID}_keywords.json', 'w', encoding="utf-8") as file:
            data = json.dump(data,file)
            
    else:
        open(f'./guild-files/{guildID}_keywords.json', 'x')
        print(str(guildID)+"_keywords.json created")
        with open(f'./guild-files/{guildID}_keywords.json', 'w', encoding='utf-8') as file:
            initData = {
                'guildID':str(guildID),
                'user':'elonmusk',
                'keywords':[],
                'activeChannelID': channelID,
                'is_active': False,
                'adminOnly': False,
                'mediaOnly': False,
                'nort': False
            }
            json.dump(initData,file)

def getKeywords(guildID):
    if os.path.exists(f'./guild-files/{guildID}_keywords.json'):
        with open(f'./guild-files/{guildID}_keywords.json', 'r', encoding="utf-8") as file:
            data = json.load(file)
            return data["keywords"]
    else:
        print(guildID+"_keywords.json does not exist")
        return 404

def getUser(guildID):
    if os.path.exists(f'./guild-files/{guildID}_keywords.json'):
        with open(f'./guild-files/{guildID}_keywords.json', 'r', encoding="utf-8") as file:
            data = json.load(file)
            return data["user"]
    else:
        print(guildID+"_keywords.json does not exist")
        return 404

def updateUser(guildID, userInput):
    if os.path.exists(f'./guild-files/{guildID}_keywords.json'):
        data = {}
        with open(f'./guild-files/{guildID}_keywords.json', 'r', encoding="utf-8") as file:
            data = json.load(file)
            data["user"] = userInput
        with open(f'./guild-files/{guildID}_keywords.json', 'w', encoding="utf-8") as file:
            data = json.dump(data,file)
    else:
        print(str(guildID)+"_keywords.json does not exist [updateUser]")
        return 404

def updatekeywords(guildID, keywordList):
    if os.path.exists(f'./guild-files/{guildID}_keywords.json'):
        data = {}
        with open(f'./guild-files/{guildID}_keywords.json', 'r', encoding="utf-8") as file:
            data = json.load(file)
            data["keywords"] = keywordList
        with open(f'./guild-files/{guildID}_keywords.json', 'w', encoding="utf-8") as file:
            data = json.dump(data,file)
    else:
        print(str(guildID)+"_keywords.json does not exist")
        return 404
        
def isAdminOnly(guildID):
  if os.path.exists(f'./guild-files/{guildID}_keywords.json'):
      with open(f'./guild-files/{guildID}_keywords.json', 'r', encoding="utf-8") as file:
          data = json.load(file)
          return data["adminOnly"]
  else:
      print(guildID+"_keywords.json does not exist")
      return 404

def isMediaOnly(guildID):
  if os.path.exists(f'./guild-files/{guildID}_keywords.json'):
      with open(f'./guild-files/{guildID}_keywords.json', 'r', encoding="utf-8") as file:
          data = json.load(file)
          return data["mediaOnly"]
  else:
      print(guildID+"_keywords.json does not exist")
      return 404

def isNort(guildID):
  if os.path.exists(f'./guild-files/{guildID}_keywords.json'):
      with open(f'./guild-files/{guildID}_keywords.json', 'r', encoding="utf-8") as file:
          data = json.load(file)
          return data["nort"]
  else:
      print(guildID+"_keywords.json does not exist")
      return 404
      
def setAdminOnly(boolVal, guildID):
  if os.path.exists(f'./guild-files/{guildID}_keywords.json'):
      data = {}
      with open(f'./guild-files/{guildID}_keywords.json', 'r', encoding="utf-8") as file:
          data = json.load(file)
          data["adminOnly"] = boolVal
      with open(f'./guild-files/{guildID}_keywords.json', 'w', encoding="utf-8") as file:
          data = json.dump(data,file)
  else:
      print(str(guildID)+"_keywords.json does not exist")
      return 404

def setMediaOnly(boolVal, guildID):
  if os.path.exists(f'./guild-files/{guildID}_keywords.json'):
      data = {}
      with open(f'./guild-files/{guildID}_keywords.json', 'r', encoding="utf-8") as file:
          data = json.load(file)
          data["mediaOnly"] = boolVal
      with open(f'./guild-files/{guildID}_keywords.json', 'w', encoding="utf-8") as file:
          data = json.dump(data,file)
  else:
      print(str(guildID)+"_keywords.json does not exist")
      return 404

def setNort(boolVal, guildID):
  if os.path.exists(f'./guild-files/{guildID}_keywords.json'):
      data = {}
      with open(f'./guild-files/{guildID}_keywords.json', 'r', encoding="utf-8") as file:
          data = json.load(file)
          data["nort"] = boolVal
      with open(f'./guild-files/{guildID}_keywords.json', 'w', encoding="utf-8") as file:
          data = json.dump(data,file)
  else:
      print(str(guildID)+"_keywords.json does not exist")
      return 404

def getActiveStatus(guildID):
    if os.path.exists(f'./guild-files/{guildID}_keywords.json'):
        with open(f'./guild-files/{guildID}_keywords.json', 'r', encoding="utf-8") as file:
            data = json.load(file)
            return data["is_active"]
    else:
        print(guildID+"_keywords.json does not exist")
        return 404