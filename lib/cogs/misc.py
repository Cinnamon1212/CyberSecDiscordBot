import discord, random
from discord.ext import commands, tasks
from itertools import cycle
from discord import Colour
from discord import AppInfo
version = "Alpha 1.0"
class misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
            print('Bot is online')

    @commands.command(name="ping", aliases=['latency'], description="Tests the latency of the bot")
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)} ms')

    @commands.command(name="version", aliases=["ver", "botversion"], description="Returns current bot version")
    async def version(self, ctx):
        embedVar = discord.Embed(title="current version", description=version, color=Colour.red())
        embedVar.add_field(name="Bot creator", value="Cinnamon#7617", inline=False)
        await ctx.send(embed=embedVar)
def setup(client):
    client.add_cog(misc(client))
