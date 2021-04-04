import discord, random
from discord.ext import commands, tasks
from itertools import cycle
from discord import Colour, Embed
from discord import AppInfo
version = "Beta 1.0"
owner = "c̸͙̪̦͛̽͝i̵̺̝͕̐͌̓n̵̞͉̪͋̾̔n̴̼̙͖̔͠a̴̺͇̦̾͊̕m̴̝͚͕͒͝͠o̸͔̼̔̐̚n̴̺͍̈́̐͝1̸̢͙͍͌͝2̵̘̘͍̿̀͘1̵͉͎͔͊͒͝2̵͎͖̞̈́̓̿"

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

    @commands.command(name="latency", aliases=['botping', 'bping'], description="Tests the latency of the bot")
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)} ms')

    @commands.command(name="botinfo", aliases=["bot", "botversion"], description="Returns information on the bot")
    async def version(self, ctx):
        embed=Embed(title=f"Information on {self.client.user}",
                    colour=discord.Colour.random())
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.add_field(name="Version: ", value=version, inline=False)
        embed.add_field(name="Number of servers: ", value=f"{len(self.client.guilds)}", inline=False)
        embed.add_field(name="Github: ", value="https://github.com/Cinnamon1212/CyberSecDiscordBot", inline=False)
        embed.set_footer(text=f"Creator: {owner}")
        await ctx.send(embed=embed)


    @commands.command(name="listofroles", description="Gives a list of roles", aliases=["roles", "serverroles"])
    async def listofroles(self, ctx):
        roles = ctx.guild.roles
        roles.reverse()
        roles.pop(-1)
        if len(roles) <= 25:
            embed = Embed(title="List of roles: ",
                          colour=discord.Colour.random())

            num = 1
            for role in roles:
                embed.add_field(name=f"Role #{num}", value=role, inline=False)
                num += 1
            time = ctx.message.created_at
            embed.set_footer(text=f"Asked by {ctx.author.name} " + time.strftime("%d/%m/%y %X"))
            await ctx.send(embed=embed)
        else:
            num = 1
            RoleList = ""
            for role in roles:
                RoleList += f"#{num} {role}\n"
                num += 1
            await ctx.send(f"```{RoleList}```")
    @commands.command(name="credits", description="Info on the bot creator!", aliases=["owner", "creator", "credit"])
    async def credits(self, ctx):
        embed = Embed(title="Credits", colour=discord.Colour.dark_purple())
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.add_field(name="Creator: ", value=owner)
        embed.add_field(name="Github: ", value="[Cinnamon1212](https://github.com/Cinnamon1212)", inline=False)
        embed.add_field(name="Patreon: ", value="[Cinnamon1212](https://www.patreon.com/cinnamon1212)", inline=False)
        embed.add_field(name="Instagram: ", value="[Cinnamon.1212](https://www.instagram.com/cinnamon.1212/)", inline=False)
        embed.set_footer(text="Feel free to check out my other projects on Github!\nAll donations are appreciated and support the bot, as well as other projects!")
        await ctx.send(embed=embed)

    @commands.command(name="invite", description="Returns invite link", aliases=["inv", "botinvite"])
    async def invite(self, ctx):
        embed = Embed(title="CyberSecurity Bot", colour=discord.Colour.random())
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.add_field(name="Shortened link: ", value="[Shortened](https://bit.ly/3fGmftl)", inline=False)
        embed.add_field(name="Full link: ", value="[Full](https://discord.com/api/oauth2/authorize?client_id=766312320589627463&permissions=8&scope=bot)", inline=False)
        time = ctx.message.created_at
        embed.set_footer(text=f"Asked by {ctx.author.name} " + time.strftime("%d/%m/%y %X"))
        await ctx.send(embed = embed)

    @commands.command(name="top.gg", description="Top.gg link", aliases=["topgg", "top"])
    async def topgg(self, ctx):
        embed = Embed(title="top.gg")
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.add_field(name="Link: ", value="[CyberSecurity Bot](https://top.gg/bot/766312320589627463)")
        time = ctx.message.created_at
        embed.set_footer(text=f"Asked by {ctx.author.name} " + time.strftime("%d/%m/%y %X"))
        await ctx.send(embed=embed)
def setup(client):
    client.add_cog(misc(client))
