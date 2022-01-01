import typing

import requests
import json
from . import client, util

global token


async def getGuild(id):
    stuff = requests.get(url=f"https://discord.com/api/v9/guilds/{id}",
                         headers={"Authorization": "Bot " + str(client.clienttoken)})
    return json.loads(stuff.content.decode("utf-8"))


async def getGuildAuditLog(id):
    checkself = await getGuildMemberPermissions(id, client.clientid, "aslist")
    if "VIEW_AUDIT_LOG" not in checkself:
        raise Exception(f"Missing Permissions For client: VIEW_AUDIT_LOG")
    stuff = requests.get(url=f"https://discord.com/api/v9/guilds/{id}/audit-logs",
                         headers={"Authorization": "Bot " + str(client.clienttoken)})
    return json.loads(stuff.content.decode("utf-8"))


async def getGuildMember(guild_id, member_id):
    stuff = requests.get(url=f"https://discord.com/api/v9/guilds/{guild_id}/members/{member_id}",
                         headers={"Authorization": "Bot " + str(client.clienttoken)})
    return json.loads(stuff.content.decode("utf-8"))


async def getGuildMemberPermissions(guild_id, member_id, type: typing.Optional = "aslist"):
    stuff = await getGuildMember(guild_id, member_id)
    match type:
        case "asbin":
            bitarray = 0b00000000000000000000000000000000000000000
            for role in stuff["roles"]:
                roledat = await getGuildRole(guild_id, role)
                print(roledat["permissions"])
                binstr = await util.permissions(roledat["permissions"], type)
                print(binstr)
                for i in range(0, len(binstr) - 1):
                    print(1 << i)
                    print(binstr)
                    print("shit:" + str(int(binstr, 2) & 1 << i))
                    if (int(binstr, 2) & (1 << i)) != 0:
                        tempbitarray = bitarray | 1 << i
                        bitarray = tempbitarray
            return bin(bitarray)
        case "aslist":
            array = []
            for role in stuff["roles"]:
                roledat = await getGuildRole(guild_id, role)
                print(roledat["permissions"])
                temparray = await util.permissions(roledat["permissions"], type)
                array = list(set(array) | set(temparray))
            return array
        case "asdict":
            array = util.fillable_permission_list
            for role in stuff["roles"]:
                roledat = await getGuildRole(guild_id, role)
                temparray = await util.permissions(roledat["permissions"], type)
                for index, item in enumerate(temparray, start=0):
                    if item["has"] is True:
                        array[index]["has"] = True
            return array


async def getGuildRoles(guild_id):
    stuff = requests.get(url=f"https://discord.com/api/v9/guilds/{guild_id}/roles",
                         headers={"Authorization": "Bot " + str(client.clienttoken)})
    return json.loads(stuff.content.decode("utf-8"))


async def getGuildRole(guild_id, role_id):
    stuff = await getGuildRoles(guild_id)
    return next(role for role in stuff if role["id"] == role_id)


async def getGuildRolePermissions(guild_id, role_id, type: typing.Optional = "aslist"):
    stuff = await getGuildRoles(guild_id)
    global tocheck
    global cancheck
    cancheck = False
    for role in stuff:
        if role["id"] == str(role_id):
            tocheck = role
            cancheck = True
            break
    if cancheck is True:
        return await util.permissions(tocheck["permissions"], type)
