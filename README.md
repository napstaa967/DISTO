# DISTO: A Really, REALLY basic Discord Api Wrapper for Python 3.10

### "Do I Seriously have To write my Own?"

Disto is a basic Discord API Wrapper written on Python 3.10, used for mking discord bots using the Discord REST API and Gateway,

Example Code:
```python
from disto import client, command

@client.event
async def on_ready(self):
    print("Ready!")

@command.command
async def ping():
    return "Pong!"

@command.subcommand("ping")
async def pong():
    return "Ping!"

client.prefix = "B:)"
client.connect("my_bot_token", intents=["list_of_intents"])
```

Docs will be added once a stable version is made