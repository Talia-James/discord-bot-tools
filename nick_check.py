#Checks to see if the user has a nickname or not
def name_check(ctx):
    try:
        if ctx.message.author.nick == None:
            sender = ctx.message.author.name
        else:
            sender = ctx.message.author.nick
    except AttributeError:
        sender = ctx.message.author.name
    return sender