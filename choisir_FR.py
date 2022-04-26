#Ajoutez ces modules au début du main.py script, ils doivent être importés avant de lancer le bot.
import random, re

#Cet outil simple choisira au hasard un élément d'une liste.
#Séparez les choix avec des virgules. Exemple: !choisir rouge, blanc, bleu, violet, orange, jaune
@bot.command()
async def choisir(ctx):
    listmake = (re.compile(r'[^,]*'))
    choices = listmake.findall(str(ctx.message.content))
    cleanedchoices = []
    #Cette fonction trouvera le nom d'utilisateur. Ce n'est pas obligatoire, on peut le supprimer tant qu'on enlève le variable <<picker>> en <<ctx.send()>>.
    if ctx.message.author.nick == None:
        picker = ctx.message.author.name
    else:
        picker = ctx.message.author.nick
    if len(choices) == 2:
        await ctx.send("Je ne peux pas choisir avec ce que vous avez saisi.")
    else:
        cleanedchoices.append((choices[0]).split()[1])
        for i in range(len(choices)):
            if choices[i] != '' and '!pick' not in choices[i]:
                stripped = choices[i].strip()
                cleanedchoices.append(stripped)
        await ctx.send(picker + ' a choisi ' + random.choice(cleanedchoices) + ' au hasard!')