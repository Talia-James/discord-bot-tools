import random

user_name = 'your_user_name_with_\# number' #Enter your user name, or the person who will be in charge of the contest, in order to prevent others from sabotaging it.
entrants = []

#This function is avoid clutter with checking for a name in every function. It will first check to see of the sender is using an alias in Discord, and if not will use their default name.
def name_check(ctx):
    if ctx.message.author.nick == None:
        sender = ctx.message.author.name
    else:
        sender = ctx.message.author.nick
    return sender

@bot.command() #This command is how users enter the contest.
async def contest(ctx):
    sender = name_check()
    global entrants
    if sender in entrants:
        await ctx.send("You've already been entered, don't cheat, @%s!" % sender)
    else:
        entrants.append(sender)
        await ctx.send("@%s added to the list!" % sender)

@bot.command() #This will draw a winner from the entrant list.
async def draw(ctx):
    if entrants != []:
        if str(ctx.message.author) == user_name:
            winner = random.choice(entrants)
            await ctx.send('%s has won. Congratuations!' % winner.mention)
        else:
            await ctx.send('You do not have permission to do that.')
    else:
        await ctx.send('The entrant list is empty.')


@bot.command() #This will clear all the entrants for a new contest. If you don't want anyone to be able to do this, then be sure to put your Discord user name into the variable.
async def clearlist(ctx):
    if str(ctx.message.author) == user_name:
        global entrants
        entrants = []
        await ctx.send('List Cleared')       
    else:
        await ctx.send('You do not have permission to do that.')