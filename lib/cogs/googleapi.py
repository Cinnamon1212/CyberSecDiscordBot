import discord, os, requests, json
from bs4 import BeautifulSoup
from discord.ext import commands
from discord import Embed
from aiohttp import request
from googleapiclient.discovery import build

with open('secrets.json', 'r') as secrets:
    data = secrets.read()
googleapikey = json.loads(data)
apikey = googleapikey['googleapi']



class googleapi(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="exploitdb", description="Search exploitdb", aliases=["exDB"])
    async def exploitdb(self, ctx, *, query):
        google = build('customsearch', 'v1', developerKey=apikey)
        search_response = google.cse().list(
            q=query,
            cx="52b54907be70ff59c"
        ).execute()
        embed = Embed(title=f"top 10 search results for {query}",
                      colour=discord.Colour.random())
        embed.set_thumbnail(url="https://www.exploit-db.com/images/spider-white.png")
        for item in search_response['items']:
            embed.add_field(name=item['title'], value=f"{item['snippet']} [Link]({item['link']})", inline=False)
        await ctx.send(embed=embed)

    @exploitdb.error
    async def exdb_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter something to query")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("No search result!")
        else:
            raise




def setup(client):
    client.add_cog(googleapi(client))
