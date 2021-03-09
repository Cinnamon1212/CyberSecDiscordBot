import discord, random
from discord.ext import commands, tasks
from itertools import cycle
from discord import Colour, Embed
from discord import AppInfo
version = "Alpha 2.0"
owner = """```
  ______                             ______ ______
 / ___(____  ___ ___ ___ _ ___  ___ <  |_  <  |_  |
/ /__/ / _ \/ _ / _ `/  ' / _ \/ _ \/ / __// / __/
\___/_/_//_/_//_\_,_/_/_/_\___/_//_/_/____/_/____/


```"""
class misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"""
 _______ __   __ ______  _______  ______      _______ _______ _______ _     _  ______ _____ _______ __   __      ______   _____  _______
 |         \_/   |_____] |______ |_____/      |______ |______ |       |     | |_____/   |      |      \_/        |_____] |     |    |
 |_____     |    |_____] |______ |    \_      ______| |______ |_____  |_____| |    \_ __|__    |       |         |_____] |_____|    |


      ______  __   __      _______ _____ __   _ __   _ _______ _______  _____  __   _
      |_____]   \_/        |         |   | \  | | \  | |_____| |  |  | |     | | \  |
      |_____]    |         |_____  __|__ |  \_| |  \_| |     | |  |  | |_____| |  \_|

        _____  __   _        _____ __   _ _______
       |     | | \  | |        |   | \  | |______
       |_____| |  \_| |_____ __|__ |  \_| |______
      
Latency: {round(self.client.latency * 1000)} ms

            """)

    @commands.command(name="latency", aliases=['botping'], description="Tests the latency of the bot")
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)} ms')

    @commands.command(name="botinfo", aliases=["bot", "botversion"], description="Returns information on the bot")
    async def version(self, ctx):
        embed=Embed(title=f"Information on {self.client.user}",
                    colour=discord.Colour.random())
        embed.set_thumbnail(url=self.client.icon_url)
        embed.add_field(name="Creator: ", value=owner, inline=True)
        embed.add_field(name="Version: ", value=version, inline=True)
        embed.add_field(name="Github: ", value="https://github.com/Cinnamon1212/CyberSecDiscordBot" , inline=True)
        await ctx.send(embed=embed)


    @commands.command(name="listofroles", description="Gives a list of roles", aliases=["roles", "serverroles"])
    async def listofroles(self, ctx):
        roles = ctx.guild.roles
        embed = Embed(title="List of roles: ",
                      colour=discord.Colour.random())

        num = 1
        roles.pop(0)
        for role in roles:
            embed.add_field(name=f"Role #{num}", value=role)
            num += 1
        time = ctx.message.created_at
        embed.set_footer(text=f"Asked by {ctx.author.name} " + time.strftime("%d/%m/%y %X"))#
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(misc(client))
