import discord, os, requests, json
from bs4 import BeautifulSoup
from discord.ext import commands
from discord import Embed
from aiohttp import request

with open('secrets.json', 'r') as secrets:
    data = secrets.read()
googleapikey = json.loads(data)
apikey = googleapikey['googleapi']



class googleapi(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="exploitdb", description="Search exploitdb", aliases=["exDB"])
    async def exploitdb(self, ctx, *, query):
        q=query,
        cx="52b54907be70ff59c"
        url = f"https://www.googleapis.com/customsearch/v1?key={apikey}&cx={cx}&q={q}&start=1"
        async with request("GET", url) as response:
            search_response = await response.json()
        embed = Embed(title=f"top 10 search results for {query}",
                      colour=discord.Colour.red())
        embed.set_thumbnail(url="https://www.exploit-db.com/images/spider-white.png")
        for item in search_response['items']:
            embed.add_field(name=item['title'], value=f"{item['snippet']} [Link]({item['link']})", inline=False)
        await ctx.send(embed=embed)

    @exploitdb.error
    async def exdb_error(self, ctx, error):
        text = "Usage: ./exdb [query]"
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"```Please enter something to query\n{text}```")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"```No search result!\n{text}```")
        else:
            raise




def setup(client):
    client.add_cog(googleapi(client))
