import inspect
from . import client, posthandler

global commandlist
commandlist = {}
subcommandlist = {}


# https://stackoverflow.com/a/26151604

def parametrized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)

        return repl

    return layer


class Commands:
    def __call__(self, commandstuff):
        if not callable(commandstuff):
            raise TypeError(f"Argument commandstuff should be 'Callable', not {type(commandstuff)}")
        commandlist[commandstuff.__name__] = commandstuff

    @parametrized
    def subcommand(command, subcommandof):
        if not callable(command):
            raise TypeError(f"Argument command should be 'Callable', not {type(command)}")
        if not isinstance(subcommandof, str):
            raise TypeError(f"Argument subcommandof should be 'str', not {type(subcommandof)}")
        subcommandlist[command.__name__] = {"upper": subcommandof, "lower": command}

    async def processcommands(self, messagecontent):

        global isbot
        isbot = False
        try:
            isbot = messagecontent["author"]["bot"]
        except (KeyError):
            isbot = False
        if isbot is True:
            return

        args = messagecontent["content"].split(" ")
        message = args[0].removeprefix(client.prefix)
        del args[0]

        if commandlist[message] is not None:
            global command
            command = commandlist[message]
            global hasremainingargs
            hasremainingargs = False
            try:
                if args[0] is not None:
                    hasremainingargs = True
            except IndexError:
                hasremainingargs = False
            if hasremainingargs is True and subcommandlist[args[0]] is not None and subcommandlist[args[0]]["upper"] == commandlist[
                message].__name__:
                command = subcommandlist[args[0]]["lower"]
                del args[0]
            topass = inspect.getfullargspec(command).args
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
                        ret_stuff = await command(args=args, msg=messagecontent)
                        alreadywaiting = True
                if alreadywaiting is False:
                    ret_stuff = await command(args=args)
                    alreadywaiting = True
            if usesfullmessage is True:
                if alreadywaiting is False:
                    ret_stuff = await command(msg=messagecontent)
                    alreadywaiting = True
            if alreadywaiting is False:
                ret_stuff = await command()
                alreadywaiting = True

            if not callable(ret_stuff):
                return posthandler.createMessage(channel=messagecontent["channel_id"],
                                                 content=ret_stuff)


command = Commands()
subcommand = Commands.subcommand
