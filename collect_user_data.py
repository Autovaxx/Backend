import json, sys, os

userDataJson = sys.argv[1]
userDataDict = json.loads(userDataJson)
print('DATA:', userDataDict)