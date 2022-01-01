# handles channel-related shit

import requests, json
from . import client, guild

supports = {
    "all": ["name", "position", "permission_overwrites"],
    "0": ["type", "topic", "nsfw", "rate_limit_per_user", "parent_id", "default_auto_archive_duration"],
    "1": [],
    "2": ["bitrate", "user_limit", "parent_id", "rtc_region", "video_quality_mode"],
    "3": ["name", "icon"],
    "4": [],
    "5": ["type", "topic", "parent_id", "default_auto_archive_duration"],
    "6": ["nsfw", "parent_id"],
    "10": ["name", "archived", "auto_archive_duration", "locked", "invitable", "rate_limit_per_user"]
}

async def getChannel(channel):
    stuff = requests.get(url=f"https://discord.com/api/v9/channels/{channel}",
                         headers={"Authorization": "Bot " + str(client.clienttoken)})
    return json.loads(stuff.content.decode("utf-8"))

async def updateChannel(channel, data):
    stuff = await getChannel(channel)
    checkself = await guild.getGuildMemberPermissions(stuff["guild_id"], client.clientid, "aslist")
    if "MANAGE_CHANNELS" not in checkself:
        raise Exception(f"Missing Permissions For client: MANAGE_CHANNELS")
    else:
        fixdata = json.loads(data)
        if not isinstance(fixdata, dict):
            raise TypeError(f"'data' Must be 'Dict', not '{type(data)}'")
        if stuff["type"] == 1:
            raise Exception("Cannot modify DM channels")
        if stuff["type"] == 4:
            raise Exception("Cannot modify Categories")
        for parameter in fixdata:
            if parameter in supports[str(stuff["type"])] or parameter in supports["all"]:
                stuff[parameter] = fixdata[parameter]
        patchstuff = requests.patch(url=f"https://discord.com/api/v9/channels/{channel}", json=stuff,
                            headers={"Authorization": "Bot " + str(client.clienttoken)})
        return patchstuff.status_code