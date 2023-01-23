#Generic calendar functions to set a game session time using the <t:[timestamp]> function in discord.
#The Discord timestamp function uses epoch time to display absolute time as an integer in epoch time, but the display will be localized according to the user's sytem locale and language.
#All functions use the format YYYY-MM-DD HH:MM in 24-hour format (1 PM = 13, etc) for non-epoch time
from datetime import datetime as dt
#If using this function for the first time, make a blank text file with the name gametime.txt in the same directory the bot is run from
@bot.command()
async def set_gametime(ctx):
    time = (ctx.message.content)[14:]
    year,month,day_hour = time.split(sep='-')
    day, hour = day_hour.split(sep=' ')
    hour,minute = hour.split(sep=':')
    epoch = dt(int(year),int(month),int(day),int(hour),int(minute)).timestamp()
    new_time = int(epoch)
    with open(f'gametime.txt','w') as f:
        f.write(str(new_time))
    #This global declaration is to share the variable with other functions. If you are only using this function then you can omit it.
    global game_time
    game_time = new_time
    await ctx.send(f'Next game at <t:{str(new_time)}>')

#This is the copied live version that switches between two game session types using an if/elif statement. The provided non-asynchronous function loads (a) .txt file(s) storing the epoch time in case the bot goes offline.
def get_times():
    with open('sw.txt','r') as f:
        global sw_time
        sw_time = int(f.readlines()[0])
    with open('coc.txt','r') as f: #Only necessary if switching between two or more game sessions
        global coc_time
        coc_time = int(f.readlines()[0])
#Necessary step in case the game falls on a Monday, in which the integer subtraction would have -1 for a day, which does not exist.
def monday_check(day):
    if day==-1:
        return 7
    else:
        return day
#Pre-defined intervals for utility
debug = 5
minutes_15 = 900
one_hour = 3600
one_day = 86400
#The function will switch between game types based on the first letter of what follows the !set_gametime command.
#If the games have similar names, provide enough spelling to the function to differentiate the two in the if/elif statements. I currently have it sliced to the first letter of the message with 
@bot.command()
async def set_gametime(ctx):
    game_and_time = (ctx.message.content)[14:] #14 is the length of the command, the relevant information in the message will always come after this.
    if game_and_time[0].lower()=='s': #Slice a character from the game_and_time string in order to differentiate between game sessions/types
        game = 'sw'
        time = game_and_time[len(game):]
        year,month,day_hour = time.split(sep='-')
        day, hour = day_hour.split(sep=' ')
        hour,minute = hour.split(sep=':')
        epoch = dt(int(year),int(month),int(day),int(hour),int(minute)).timestamp()
        new_time = int(epoch)
        with open(f'{game}.txt','w') as f:
            f.write(str(new_time))
        global sw_time
        sw_time = new_time
        await ctx.send(f'Next Star Wars game at <t:{str(new_time)}>')
    elif game_and_time[0].lower()=='c':
        game='coc'
        time = game_and_time[len(game):]
        year,month,day_hour = time.split(sep='-')
        day, hour = day_hour.split(sep=' ')
        hour,minute = hour.split(sep=':')
        epoch = dt(int(year),int(month),int(day),int(hour),int(minute)).timestamp()
        new_time = int(epoch)
        with open(f'{game}.txt','w') as f:
            f.write(str(new_time))
        global coc
        coc = new_time
        await ctx.send(f'Next Call of Cthulhu game at <t:{str(new_time)}>')

#Provides an epoch integer timestamp to be used with the discord <t:[timestamp]> functionality.
#Uses the format YYYY-MM-DD HH:MM in 24-hour format (1 PM = 13, etc)
@bot.command()
async def stamp(ctx):
    time = ctx.message.content[7:]
    year,month,day_hour = time.split(sep='-')
    day, hour = day_hour.split(sep=' ')
    hour,minute = hour.split(sep=':')
    epoch = dt(int(year),int(month),int(day),int(hour),int(minute)).timestamp()
    new_time = int(epoch)
    await ctx.send(new_time)

#Finds the session time for the provided game type.
#The "game" variable is the same as the .txt file holding the epoch time integer.
#For example, if the game is named dnd5e, then the .txt file holding the game time should be dnd5e.txt
@bot.command()
async def gametime(ctx):
    game = (ctx.message.content)[10:]
    with open(f'{game}.txt','r') as f:
        time = f.readlines()[0]
    await ctx.send(f'Next {game} session is at <t:{time}>, <t:{time}:R>')

#If only one game session is ever used/needed, this generic version can be used.
#Note the filename is the same as the one created in the set_gametime function. If using both functions, the names should match.
@bot.command()
async def gametime(ctx):
    game = 'gametime'
    with open(f'{game}.txt','r') as f:
        time = f.readlines()[0]
    await ctx.send(f'Next session is at <t:{time}>, <t:{time}:R>')

#NB: <t:[timestamp]> will provide the locale-specific time to the user in the format
# [Month name] [date], [year], [12-hour time] [AM/PM]
# <t:[timestamp]:R> will provide a relative duration from the locale time to/from the timestamped date.
# EX: "2 days ago", "In 6 hours", etc 