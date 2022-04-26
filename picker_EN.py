#Add these packages to the beginning of the main.py script, they must be imported before launching the bot
import random, re

#This simple function will randomly choose one item from a list.
#Separate choices by commas. Example: !pick red, white, blue, purple, orange, yellow
@bot.command()
async def pick(ctx):
    listmake = (re.compile(r'[^,]*'))
    choices = listmake.findall(str(ctx.message.content))
    cleanedchoices = []
    #This check will assign a name for the bot to respond to. It can be removed so long as the 'picker' variable is removed from the return.
    if ctx.message.author.nick == None:
        picker = ctx.message.author.name
    else:
        picker = ctx.message.author.nick
    if len(choices) == 2:
        await ctx.send("I am unable to make a choice without a choice.")
    else:
        cleanedchoices.append((choices[0]).split()[1])
        for i in range(len(choices)):
            if choices[i] != '' and '!pick' not in choices[i]:
                stripped = choices[i].strip()
                cleanedchoices.append(stripped)
        await ctx.send(picker + ' has randomly chosen ' + random.choice(cleanedchoices) + '!')