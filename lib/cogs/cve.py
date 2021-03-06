import discord, os, requests
from discord.ext import commands
from discord import Embed
from aiohttp import request

class cve(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="cvesearch", description="Search", alises=["cveid", "cvelookup"])
    async def cvesearch(self, ctx, cveid):
        if cveid == "":
            await ctx.send("Please provide a cve ID")
        else:
            url = "https://cve.circl.lu/api/cve/" + cveid
            async with request("GET", url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    embed = Embed(title=f"Info on {cveid}",
                                  description=f"Name: {data['capec'][0]['name']}",
                                  colour=discord.Colour.random(),
                                  inline=True)
                    embed.add_field(name="Authentication: ", value=data['access']['authentication'], inline=True)
                    embed.add_field(name="Complexity: ", value=data['access']['complexity'], inline=True)
                    embed.add_field(name="Vector: ", value=data['access']['vector'], inline=True)
                    embed.add_field(name="Summary: ", value=data['capec'][0]['summary'], inline=True)
                    embed.add_field(name="Solutions: ", value=data['capec'][0]['solutions'], inline=True)

                    time = ctx.message.created_at
                    embed.set_footer(text=f"Asked by {ctx.author.name} " + time.strftime("%d/%m/%y %X"))

                    await ctx.send(embed=embed)
def setup(client):
    client.add_cog(cve(client))
