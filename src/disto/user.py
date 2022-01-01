import requests
import json
global token

async def getUser(id):
    stuff = requests.get(url=f"https://discord.com/api/v9/users/{id}", headers={"Authorization": "Bot " + str(token)})
    return json.loads(stuff.content.decode("utf-8"))

async def getUserPermissions(id):
    stuff = requests.get(url=f"https://discord.com/api/v9/users/{id}", headers={"Authorization": "Bot " + str(token)})
    return json.loads(stuff.content.decode("utf-8"))

