#Add these packages to the beginning of the main.py script, they must be imported before launching the bot
import random, re

#This tool will 'roll' an N-sided die X amount of times with +Y added as a modifier. It uses regular expressions to parse the user input.
#The syntax is !roll XdN+Y. For example, !roll 4d10+5 will roll 4 10-sided die, sum their results, and add 5 to the final total. '-' can also be used to subtract.
@bot.command()
async def roll(ctx):
    #This check will assign a name for the bot to respond to. It can be removed so long as the 'sender' variable is removed from the return.
    if ctx.message.author.nick == None:
        sender = ctx.message.author.name
    else:
        sender = ctx.message.author.nick
    diesearch = re.compile(r'(\d+)(d)*(\d*)([+/-]\d*)?', re.I)
    userinput = ctx.message.content
    diceformat = diesearch.search(userinput)
    try:
        diceformat[4] == None
        modifier = int(diceformat[4][1:])
        sign = diceformat[4][0]
    except TypeError:
        modifier = 0
        sign = ''
    if diceformat.group(2) is None:
        dN = int(diceformat.group(1))
        print(type(diceformat.group(0)))
        dice = random.randint(1, dN)
        print('-' in diceformat.group(0))
        if '-' in diceformat.group(0):
            await ctx.send(sender + ' rolled ' + str(dice - modifier) + ' from a d' + str(dN - modifier) + '!')
        elif '+' in diceformat.group(0):
            await ctx.send(sender + ' rolled ' + str(dice + modifier) + ' from a d' + str(dN + modifier) + '!')
        else:
            await ctx.send(sender + ' rolled ' + str(dice) + ' from a d' + str(dN) + '!')
    elif diceformat.group(3) == '':
        sign = diceformat[4][0]
        dN = int(diceformat.group(1))
        dice = random.randint(1, dN)
        if sign == '-':
            await ctx.send(sender + ' rolled ' + str(dice - modifier) + ' from a d' + str(dN - modifier) + '!')
        else:
            await ctx.send(sender + ' rolled ' + str(dice + modifier) + ' from a d' + str(dN + modifier) + '!')        
    else:
        dN = int(diceformat.group(3))
        multiplier = int(diceformat.group(1))
        amt = 0
        for _ in range(multiplier):
            amt += random.randint(1, dN)
        if sign == '-':
            await ctx.send(sender + ' rolled ' + str(amt - modifier) + ' out of a possible ' + str((dN * multiplier)-modifier) + '!')
        else:
            await ctx.send(sender + ' rolled ' + str(amt + modifier) + ' out of a possible ' + str((dN * multiplier)+modifier) + '!')