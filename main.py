#Required packages for core functionality
import discord
from discord.ext import commands

#Necessary to set permissions
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!',intents=intents) #command_prefix sets the character the user needs to type in order to call a bot function. In this example a user would type '!' followed by a custom function to use the bot
client = discord.Client(intents=intents)
intents.members = True

#This message will print to the terminal when the bot is online and ready to function
@bot.event
async def on_ready():
    print('Bot ready.')

#Replace 'Personal token' with the bot token from your own Discord developer account. Make sure the token itself remains a string.
bot.run('Personal token')