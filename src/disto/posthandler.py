import requests
global token

def createMessage(channel, content):
    global body
    if isinstance(content, dict) is True:
        body = content
    else:
        body = {
          "content": content
        }
    requests.post(url=f"https://discord.com/api/v9/channels/{channel}/messages", json=body, headers={"Authorization": "Bot " + str(token)})



