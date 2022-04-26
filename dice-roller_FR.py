#Ajoutez ces modules au début du main.py script, ils doivent être importés avant de lancer le bot.
import random, re

#Cet outil <<roulera>> un dé avec N côtés X fois avec Y ajouté à la somme finale. Il utilise les expression régulières pour analyser la saisie de l'utilisateur.
#La syntaxe est !rouler XdN+Y. Par exemple, !rouler 4d10+5 roulera 4 dés avec 10 côtés, ajoutera leur résultats, et puis ajoutera 5 à la somme finale. '-' peut aussi servir pour soustraire.
@bot.command()
async def rouler(ctx):
    #Cette fonction trouvera le nom d'utilisateur. Ce n'est pas obligatoire, on peut le supprimer tant qu'on enlève des commandes <<ctx.send()>>.
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
            await ctx.send(sender + ' a roulé ' + str(dice - modifier) + ' sur un dé ' + str(dN - modifier) + '!')
        elif '+' in diceformat.group(0):
            await ctx.send(sender + ' a roulé ' + str(dice + modifier) + ' sur un dé ' + str(dN + modifier) + '!')
        else:
            await ctx.send(sender + ' a roulé ' + str(dice) + ' sur un dé ' + str(dN) + '!')
    elif diceformat.group(3) == '':
        sign = diceformat[4][0]
        dN = int(diceformat.group(1))
        dice = random.randint(1, dN)
        if sign == '-':
            await ctx.send(sender + ' a roulé ' + str(dice - modifier) + ' sur un dé ' + str(dN - modifier) + '!')
        else:
            await ctx.send(sender + ' a roulé ' + str(dice + modifier) + ' sur un dé ' + str(dN + modifier) + '!')        
    else:
        dN = int(diceformat.group(3))
        multiplier = int(diceformat.group(1))
        amt = 0
        for _ in range(multiplier):
            amt += random.randint(1, dN)
        if sign == '-':
            await ctx.send(sender + ' a roulé ' + str(amt - modifier) + ' sur un total possible ' + str((dN * multiplier)-modifier) + '!')
        else:
            await ctx.send(sender + ' a roulé ' + str(amt + modifier) + ' sur un total possible ' + str((dN * multiplier)+modifier) + '!')