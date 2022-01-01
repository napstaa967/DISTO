import typing

from bitstring import BitArray

permission_list = permsarray = [
    "CREATE_INSTANT_INVITE", "KICK_MEMBERS", "BAN_MEMBERS", "ADMINISTRATOR", "MANAGE_CHANNELS", "MANAGE_GUILD",
    "ADD_REACTIONS", "VIEW_AUDIT_LOG", "PRIORITY_SPEAKER", "STREAM", "VIEW_CHANNEL", "SEND_MESSAGES",
    "SEND_TTS_MESSAGES", "MANAGE_MESSAGES", "EMBED_LINKS", "ATTACH_FILES", "READ_MESSAGE_HISTORY", "MENTION_EVERYONE",
    "USE_EXTERNAL_EMOJIS", "VIEW_GUILD_INSIGHTS", "CONNECT", "SPEAK", "MUTE_MEMBERS", "DEAFEN_MEMBERS", "MOVE_MEMBERS",
    "USE_VAD", "CHANGE_NICKNAME",
    "MANAGE_NICKNAMES", "MANAGE_ROLES", "MANAGE_WEBHOOKS", "MANAGE_EMOJIS_AND_STICKERS", "USE_APPLICATION_COMMANDS",
    "REQUEST_TO_SPEAK", "MANAGE_EVENTS", "MANAGE_THREADS", "CREATE_PUBLIC_THREADS", "CREATE_PRIVATE_THREADS",
    "USE_EXTERNAL_STICKERS", "SEND_MESSAGES_IN_THREADS", "START_EMBEDDED_ACTIVITIES", "MODERATE_MEMBERS", ]

fillable_permission_list = [{
    "name": "CREATE_INSTANT_INVITE",
    "has": False
}, {
    "name": "KICK_MEMBERS",
    "has": False
}, {
    "name": "BAN_MEMBERS",
    "has": False
}, {
    "name": "ADMINISTRATOR",
    "has": False
}, {
    "name": "MANAGE_CHANNELS",
    "has": False
}, {
    "name": "MANAGE_GUILD",
    "has": False
}, {
    "name": "ADD_REACTIONS",
    "has": False
}, {
    "name": "VIEW_AUDIT_LOG",
    "has": False
}, {
    "name": "PRIORITY_SPEAKER",
    "has": False
}, {
    "name": "STREAM",
    "has": False
}, {
    "name": "VIEW_CHANNEL",
    "has": False
}, {
    "name": "SEND_MESSAGES",
    "has": False
}, {
    "name": "SEND_TTS_MESSAGES",
    "has": False
}, {
    "name": "MANAGE_MESSAGES",
    "has": False
}, {
    "name": "EMBED_LINKS",
    "has": False
}, {
    "name": "ATTACH_FILES",
    "has": False
}, {
    "name": "READ_MESSAGE_HISTORY",
    "has": False
}, {
    "name": "MENTION_EVERYONE",
    "has": False
}, {
    "name": "USE_EXTERNAL_EMOJIS",
    "has": False
}, {
    "name": "VIEW_GUILD_INSIGHTS",
    "has": False
}, {
    "name": "CONNECT",
    "has": False
}, {
    "name": "SPEAK",
    "has": False
}, {
    "name": "MUTE_MEMBERS",
    "has": False
}, {
    "name": "DEAFEN_MEMBERS",
    "has": False
}, {
    "name": "MOVE_MEMBERS",
    "has": False
}, {
    "name": "USE_VAD",
    "has": False
}, {
    "name": "CHANGE_NICKNAME",
    "has": True
}, {
    "name": "MANAGE_NICKNAMES",
    "has": False
}, {
    "name": "MANAGE_ROLES",
    "has": False
}, {
    "name": "MANAGE_WEBHOOKS",
    "has": False
}, {
    "name": "MANAGE_EMOJIS_AND_STICKERS",
    "has": False
}, {
    "name": "USE_APPLICATION_COMMANDS",
    "has": False
}, {
    "name": "REQUEST_TO_SPEAK",
    "has": False
}, {
    "name": "MANAGE_EVENTS",
    "has": False
}, {
    "name": "MANAGE_THREADS",
    "has": False
}, {
    "name": "CREATE_PUBLIC_THREADS",
    "has": False
}, {
    "name": "CREATE_PRIVATE_THREADS",
    "has": False
}, {
    "name": "USE_EXTERNAL_STICKERS",
    "has": False
}, {
    "name": "SEND_MESSAGES_IN_THREADS",
    "has": False
}, {
    "name": "START_EMBEDDED_ACTIVITIES",
    "has": False
}, {
    "name": "MODERATE_MEMBERS",
    "has": False
}]


async def permissions(perms, type: typing.Optional = "aslist"):
    stuff = bin(int(perms))
    stuff2 = BitArray(bin=stuff)
    permissions_dict = fillable_permission_list
    permissions_list = []
    for i in range(0, len(stuff2) - 1):
        if int(perms) & (1 << i):
            permissions_dict[i]["has"] = True
            permissions_list.append(permissions_dict[i]["name"])
    match type:
        case "asdict":
            return permissions_dict
        case "aslist":
            return permissions_list
        case "asbin":
            print("stuff" + stuff)
            return stuff
