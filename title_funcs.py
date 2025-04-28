#Functions for session title tools. Variables need to be instantiated on initial bot startup.
import nick_check as name_check #Required for personalization of response message. Remove name_check lines and {sender} variable from its respective line if you do not want this function.
import csv, collections
import pandas as pd
entrants = []
showtitles = {}
votes = []
index = 1

#Loads titles from .csv file in case of bot interruption
def load_titles():
    with open('titles.csv',newline='') as f:
        reader = csv.reader(f,delimiter=',')
        i=0
        for row in reader:
            if i==0:
                titles_ = row
                i+=1
            else:
                pass
    return titles_

#Refreshes titles, removing all previous entries.
@bot.command()
async def refresh(ctx):
    global votes
    votes = []
    with open('titles.csv','w') as f:
        writer = csv.writer(f)
        writer.writerow('')
    with open('vote_hist.csv','w') as f:
        writer = csv.writer(f)
        writer.writerow('')
    with open('votes.csv','w') as f:
        writer = csv.writer(f)
        writer.writerow('')
    sender = name_check(ctx)
    global vote_hist
    vote_hist = []
    await ctx.send(f'List purged, Captain {sender}.')

#Submit a title. Inspired by Showbot https://www.showbot.tv/
@bot.command()
async def s(ctx):
    sender = name_check(ctx)
    title = (ctx.message.content)[3:]
    titles = load_titles()
    titles.append(title)
    with open('titles.csv','w') as f:
        writer = csv.writer(f)
        writer.writerow(titles)
    await ctx.send('Titled added, Captain ' + sender)

#Display all titles submitted so far. Functions in a main channel or direct message with the bot.
@bot.command()
async def titles(ctx):
    titles_ = load_titles()
    title_list = []
    for i in range(len(titles_)):
        title_list.append(str(i+1)+': '+str(titles_[i]))
    await ctx.send('\n'.join(title_list))

#Use !vote [x] where [x] is the number of the title you wish to vote for. Must only use one number at a time. You can vote for multiple titles but must type !vote [x] each time.
@bot.command(pass_context=True)
async def vote(ctx):
    sender = name_check(ctx)
    vote = ctx.message.content[6:]
    vote_entry = f'{sender}-{vote}'
    with open("vote_hist.csv",'r') as f:
        reader = csv.reader(f,delimiter=',')
        i=0
        for row in reader:
            if i==0:
                vote_hist = row
                i+=1
            else:
                pass
    try:
        if vote_entry in vote_hist:
            await ctx.send(f'You have already voted for that title, Captain {sender}.')
        else:
            numvote = int(vote)
            votes.append(numvote)
            with open('votes.csv','w') as f:
                writer = csv.writer(f)
                writer.writerow(votes)
            vote_hist.append(vote_entry)
            with open('vote_hist.csv','w') as f:
                writer = csv.writer(f)
                writer.writerow(vote_hist)
            await ctx.send(f'Vote recorded, Captain {sender}.')
    except ValueError:
        await ctx.send(f'That is not a number, Captain {sender}.')

#Show the winning title(s) that received the most votes
@bot.command(pass_context=True)
async def votecount(ctx):
    with open("votes.csv",'r') as f:
        reader = csv.reader(f,delimiter=',')
        j=0
        for row in reader:
            if j==0:
                votes_ = row
                j+=1
            else:
                pass
    votecount = collections.Counter(votes_)
    showtitles = load_titles()
    df = pd.Series(votecount).sort_values(ascending=False)
    send_titles = [f'{df.iloc[i]}: {showtitles[int(df.index[i])-1]}' for i in range(len(df))]
    await ctx.send('\n'.join(send_titles))