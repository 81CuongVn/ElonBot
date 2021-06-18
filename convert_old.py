import os
import json
import csv

#converts old v1.2 or older csv and json files to v1.3. (adds new key and moves to guild-files folder)
for oldfile in os.listdir():
  if "_keywords.json" in oldfile:
    oldData = {}
    with open(oldfile, "r") as jsonFile:
      oldData = json.load(jsonFile)
    
    oldData['adminOnly'] = False
    
    with open(f'./guild-files/{oldfile[:-14]}_keywords.json', 'x') as jsonFile:
      json.dump(oldData, jsonFile)
      
for oldfile in os.listdir():
  if "_lastIDs.csv" in oldfile:
    oldData = []
    with open(oldfile, "r") as csvFile:
      reader = csv.reader(csvFile)
      oldData = list(reader)
    with open(f'./guild-files/{oldfile[:-12]}_lastIDs.csv', 'x') as csvFile:
      writer = csv.writer(csvFile)
      writer.writerows(oldData)