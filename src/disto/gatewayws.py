# Do I Seriously have To write my Own

# This controls the websocket used to connect to the gateway

import requests
from . import posthandler, user, client, command
import ast
import random
import json
import asyncio
import websockets

# using API v9, for latest stuff

global url
url: str = 'https://discord.com/api/v9'


def get_connection_url(bot_token):
    response = requests.get(url=str(url) + "/gateway/bot",
                            headers={"Authorization": "Bot " + str(bot_token)})
    # stackoverflow https://stackoverflow.com/a/49184648
    result = ast.literal_eval(response.content.decode("UTF-8"))
    return result['url']


def start(bot_token, intents):
    posthandler.token = bot_token
    user.token = bot_token
    client.clienttoken = bot_token
    global ints
    ints = intents

    async def websocket():
        uri = f"{get_connection_url(bot_token)}/?v=9&encoding=json"
        global auth
        auth = False
        global localheartbeat
        localheartbeat = 0
        global heartbeats
        heartbeats = 0
        async with websockets.connect(uri) as websocket:
            # identify client first things first
            # on message request from the discord gateway
            async for message in websocket:
                data = message
                filtered = json.loads(data)
                # send initial heartbeat
                # if filtered["t"] == "READY":
                # send event data to client file
                match filtered["t"]:
                    case "READY":
                        client.clientid = filtered["d"]["user"]["id"]
                        await client.Events.client_ready(client.Events)
                    case "MESSAGE_CREATE":
                        await client.Events.message_post(client.Events, filtered["d"])
                        if len(command.commandlist) > 0:
                            asyncio.create_task(command.Commands.processcommands(command.Commands, filtered["d"]))

                if filtered["op"] == 10:
                    # initial heartbeat on gateway hello event
                    jitter = random.uniform(0, 1)
                    localheartbeat = (filtered["d"]["heartbeat_interval"] / 1000)
                    # time.sleep((filtered["d"]["heartbeat_interval"] / 1000) * jitter)
                    await websocket.send('{"op": 1,"d": 251}')

                if filtered["op"] == 1:
                    # incase gateway requests an inmediate heartbeat
                    await websocket.send('{"op": 1,"d": 251}')

                if filtered["op"] == 11 and auth is True:
                    async def heartbeat():
                        await asyncio.sleep(localheartbeat)
                        await websocket.send('{"op": 1,"d": 251}')

                    asyncio.create_task(heartbeat())
                if filtered["op"] == 11 and auth is False:
                    finalintents = 0
                    for tent in ints:
                        match tent:
                            case "GUILDS":
                                finalintents += 1 << 0
                            case "GUILD_MEMBERS":
                                finalintents += 1 << 1
                            case "GUILD_BANS":
                                finalintents += 1 << 2
                            case "GUILD_EMOJIS_AND_STICKERS":
                                finalintents += 1 << 3
                            case "GUILD_INTEGRATIONS":
                                finalintents += 1 << 4
                            case "GUILD_WEBHOOKS":
                                finalintents += 1 << 5
                            case "GUILD_INVITES":
                                finalintents += 1 << 6
                            case "GUILD_VOICE_STATES":
                                finalintents += 1 << 7
                            case "GUILD_PRESENCES":
                                finalintents += 1 << 8
                            case "GUILD_MESSAGES":
                                finalintents += 1 << 9
                            case "GUILD_MESSAGE_REACTIONS":
                                finalintents += 1 << 10
                            case "GUILD_MESSAGE_TYPING":
                                finalintents += 1 << 11
                            case "DIRECT_MESSAGES":
                                finalintents += 1 << 12
                            case "DIRECT_MESSAGE_REACTIONS":
                                finalintents += 1 << 13
                            case "DIRECT_MESSAGE_TYPING":
                                finalintents += 1 << 14
                            case "GUILD_SCHEDULED_EVENTS":
                                finalintents += 1 << 16
                    await websocket.send(
                        '{"op": 2,"d":{"token": "' + bot_token + '","intents": ' + str(finalintents) + ',"properties": {"$os": "linux", "$browser": "disto","$device": "disto"}}}')
                    await websocket.send('{"op": 1,"d": 251}')
                    auth = True

    asyncio.get_event_loop().run_until_complete(websocket())
    asyncio.get_event_loop().run_forever()
