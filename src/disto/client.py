# Client code
# This triggers on every websocket event that happens on gateway_connection
import typing
from . import gatewayws

global prefix
global clienttoken
global intents_used
global clientid


def connect(bot_token, bot_prefix: typing.Optional[str] = "./",
            intents: typing.Optional = ["GUILDS", "GUILD_MESSAGES"]):
    gatewayws.start(bot_token, intents)
    intents_used = intents
    clienttoken = bot_token

    prefix = bot_prefix


class Events:
    async def message_post(self, message_content):
        return

    async def client_ready(self):
        return


# event replacer
def event(new):
    match new.__name__:
        case "message_post" | "on_message":
            Events.message_post = new
        case "on_ready" | "ready" | "client_ready0":
            Events.client_ready = new
