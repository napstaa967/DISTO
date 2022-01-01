import inspect
from . import client, posthandler

global commandlist
commandlist = []
subcommandlist = []


# https://stackoverflow.com/a/26151604

def parametrized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)

        return repl

    return layer


class Commands:
    def __call__(self, commandstuff):
        commandlist.append(commandstuff)

    @parametrized
    def subcommand(command, subcommandof):
        subcommandlist.append({"upper": subcommandof, "lower": command})

        # i hate python

    async def processcommands(self, messagecontent):

        global isbot
        isbot = False
        try:
            isbot = messagecontent["author"]["bot"]
        except (KeyError):
            isbot = False
        if isbot is True:
            return

        preargs = messagecontent["content"].split(" ")
        premessage = preargs[0]
        args = preargs
        del args[0]
        message = premessage.removeprefix(client.prefix)
        for command in commandlist:
            cmd = str(command.__name__)
            # Catch command args, check if subcommand, use subcommand if true
            global torun
            torun = command
            global subcom
            subcom = ""
            for subc in subcommandlist:
                if subc["upper"] == cmd and args[0] == subc["lower"].__name__:
                    torun = subc["lower"]
                    subcom = subc["upper"]
            if (message == torun.__name__) or (message == subcom and args[0] == torun.__name__):
                if len(args) > 0:
                    if args[0] == torun.__name__:
                        del args[0]
                fullcmd = torun
                topass = inspect.getfullargspec(torun).args
                global usesargs
                usesargs = False
                global usesfullmessage
                usesfullmessage = False

                if "args" in topass:
                    usesargs = True
                if "msg" in topass:
                    usesfullmessage = True
                global ret_stuff
                global alreadywaiting
                alreadywaiting = False
                if usesargs is True:
                    if usesfullmessage is True:
                        if alreadywaiting is False:
                            ret_stuff = await fullcmd(args=args, msg=messagecontent)
                            alreadywaiting = True
                    if alreadywaiting is False:
                        ret_stuff = await fullcmd(args=args)
                        alreadywaiting = True
                if usesfullmessage is True:
                    if alreadywaiting is False:
                        ret_stuff = await fullcmd(msg=messagecontent)
                        alreadywaiting = True
                if alreadywaiting is False:
                    ret_stuff = await fullcmd()
                    alreadywaiting = True

                if not callable(ret_stuff):
                    return posthandler.createMessage(channel=messagecontent["channel_id"],
                                                     content=ret_stuff)


command = Commands()
subcommand = Commands.subcommand
