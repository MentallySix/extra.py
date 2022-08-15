import http.client
import discord
from discord.ui import Button , View , Select
from discord.ext import commands
from discord.ext import tasks
from discord.utils import find
import random
import asyncio
import asyncpraw
import requests
from aiohttp import ClientSession


wyr = http.client.HTTPSConnection("would-you-rather.p.rapidapi.com")
wyr_headers = {
    'X-RapidAPI-Key': "5c01aad652mshd00f3d060029ce8p19a4d9jsn6865d9b6d5cc",
    'X-RapidAPI-Host': "would-you-rather.p.rapidapi.com"
    }

'''define = http.client.HTTPSConnection("mashape-community-urban-dictionary.p.rapidapi.com")
define_headers = {
    'X-RapidAPI-Key':'5c01aad652mshd00f3d060029ce8p19a4d9jsn6865d9b6d5cc',
    'X-RapidAPI-Host': "mashape-community-urban-dictionary.p.rapidapi.com"
}'''



async def embeding(ctx,title,description,colourr):
    if colourr == 'red':
        embed = discord.Embed(title=title,description=description,color = discord.Color.red())
    elif colourr == 'green':
        embed = discord.Embed(title=title,description=description,color = discord.Color.green())
    elif colourr == 'blue':
        embed = discord.Embed(title=title,description=description,color = discord.Color.blue())
    elif colourr == 'orange':
        embed = discord.Embed(title=title,description=description,color = discord.Color.orange())
    elif colourr == 'random':
        embed = discord.Embed(title=title,description=description,color= discord.Color.random())
    return embed

class extra(commands.Cog):
    def __init__(self, bot):
        self.bot = bot    
    
    @commands.command()
    async def wyr(self,ctx):
        response = False
        while response == False:
            try:
                wyr.request("GET", "/wyr/random", headers=wyr_headers)
                res = wyr.getresponse()
                data = res.read()
                data = str(data.decode("utf-8"))
                data= data.replace('[','')
                data= data.replace(']','')
                data= data.replace('question','')
                data= data.replace(':','')
                data= data.replace('{','')
                data= data.replace('}','')
                data= data.replace('"','')
                msg = await ctx.send(embed=await embeding(ctx,'Would You Rather',data,'random'))
                await msg.add_reaction('1️⃣')
                await msg.add_reaction('2️⃣')
                response = True
            except:
                pass

    @commands.command()
    async def searchimage(self,ctx,subred='cat'):
        msg = await ctx.send('Loading message..<a:loading:1002540830994735165> ')
        reddit = asyncpraw.Reddit(client_id="VKDfpU-AT8xcvPbCuHps1Q",client_secret="WcFfFqZoBMpamLY_cF4LSzFbqb0wRw",user_agent="praw")
        subreddit = await reddit.subreddit(subred)
        tries = 0
        while tries < 4:
            if subreddit == []:
                await msg.edit('Subreddit not found!')
                break
            try:
                all_subs = []
                async for submission in subreddit.new(limit = 100):        
                    all_subs.append(submission)
                random_sub = random.choice(all_subs)
                name = random_sub.title
                url = random_sub.url
                embed = discord.Embed(title=name,colour=discord.Color.random(),description=url)
                embed.set_image(url=url)
                await msg.edit('',embed=embed)
                break 
            except:
                tries += 1
        if tries == 4: await msg.edit('Error!')


    @commands.command()
    async def search(self,ctx,subred='AmItheAsshole?'):
        msg = await ctx.send('Loading message..<a:loading:1002540830994735165> ')
        reddit = asyncpraw.Reddit(client_id="VKDfpU-AT8xcvPbCuHps1Q",client_secret="WcFfFqZoBMpamLY_cF4LSzFbqb0wRw",user_agent="praw")
        subreddit = await reddit.subreddit(subred)

        all_subs = []
        async for submission in subreddit.new(limit = 100):        
            all_subs.append(submission)
            random_sub = random.choice(all_subs)                
            name = random_sub.title
            url = random_sub.url
            embed = discord.Embed(title=name,colour=discord.Color.random(),description=random_sub.selftext)
        await msg.edit('',embed=embed)
        response = True
          




    @commands.command()
    async def define(self,ctx,*,term):
        url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
        querystring = {"term":term}
        headers = {
        'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
        'x-rapidapi-key': "5c01aad652mshd00f3d060029ce8p19a4d9jsn6865d9b6d5cc"
        }
        async with ClientSession() as session:
            async with session.get(url, headers=headers, params=querystring) as response:
                r = await response.json()
                definition = r['list'][0]['definition']
                example = r['list'][0]['example']
                likes= r['list'][0]['thumbs_up']
                dislikes= r['list'][0]['thumbs_down']
                embed = discord.Embed(title=term, description=definition,color=discord.Color.random()) # <- [1]
                embed.add_field(name='Example:',value=example)
                embed.set_footer(text=f"Written by {r['list'][0]['author']}")
                view = View()
                likes = Button(label = likes , style = discord.ButtonStyle.green,emoji = '👍')
                dislikes = Button(label = dislikes , style = discord.ButtonStyle.red,emoji = '👎')
                view.add_item(likes)
                view.add_item(dislikes)
                await ctx.send(embed=embed,view=view) 

    @commands.command()
    async def sendmeme(self,ctx):
        subred= ['dankvideos','perfectlycutscreams','holdmybeer','unexpected','AnimalsBeingDerps','fixedbytheduet']
        reddit = asyncpraw.Reddit(client_id="VKDfpU-AT8xcvPbCuHps1Q",client_secret="WcFfFqZoBMpamLY_cF4LSzFbqb0wRw",user_agent="praw")
        for x in range(10):
            random_sub = random.choice(subred)
            subreddit = await reddit.subreddit(random_sub)
            all_subs = []
            async for submission in subreddit.new(limit = 100):        
                all_subs.append(submission)
                random_sub = random.choice(all_subs)        
            url = random_sub.url
            url= url.replace('https://v.redd.it/','')       
            url= '<https://redditsave.com/info?url=https%3A%2F%2Fv.redd.it%2F'+url+'>'
            await ctx.send(url)






async def setup(bot):
    await bot.add_cog(extra(bot))