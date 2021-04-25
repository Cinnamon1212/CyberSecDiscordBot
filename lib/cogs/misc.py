import discord, random, time, datetime, sys, platform, math, psutil, os, subprocess
from discord.ext import commands, tasks
from itertools import cycle
from discord import Colour, Embed
from discord import AppInfo
from pygicord import Paginator

start_time = time.time()
version = "Beta 3.1"
owner = "c̸͙̪̦͛̽͝i̵̺̝͕̐͌̓n̵̞͉̪͋̾̔n̴̼̙͖̔͠a̴̺͇̦̾͊̕m̴̝͚͕͒͝͠o̸͔̼̔̐̚n̴̺͍̈́̐͝1̸̢͙͍͌͝2̵̘̘͍̿̀͘1̵͉͎͔͊͒͝2̵͎͖̞̈́̓̿"
torversion = subprocess.check_output("tor --version", shell=True).decode()

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

    @commands.command(name="listofroles", description="Gives a list of roles", aliases=["roles", "serverroles"])
    async def listofroles(self, ctx):
        def get_pages(pagescount, roles):
            z = 1
            pages = []
            x = 1
            for i in range(1, pagecount + 1):
                embed = Embed(title=f"{ctx.message.guild.name} roles", colour=discord.Colour.random())
                embed.set_footer(text=f"Page {x}/{pagecount}")
                x += 1
                for role in roles[x - 2]:
                    embed.add_field(name=f"#{z}", value=role.name)
                    z += 1
                pages.append(embed)
            return pages

        roles = ctx.guild.roles
        roles.reverse()
        roles.pop(-1)
        roleslist = [roles[x:x+25] for x in range(0, len(roles), 25)]
        pagecount = math.ceil(len(roles) / 25)
        paginator = Paginator(pages=get_pages(pagecount, roleslist))
        await paginator.start(ctx)

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

    @commands.command(name="stats", description="Bot statistics", aliases=["statistics", "botstats", "botinfo", "bot", "version"])
    async def stats(self, ctx):
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed=Embed(title=f"{self.client.user} stats",
                    colour=discord.Colour.random())
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.add_field(name="Uptime: ", value=text, inline=False)
        embed.add_field(name="Version: ", value=version, inline=False)
        embed.add_field(name="Number of servers: ", value=len(self.client.guilds), inline=False)
        embed.add_field(name="Online users: ", value=str(len({m.id for m in self.client.get_all_members() if m.status is not discord.Status.offline})), inline=False)
        embed.add_field(name="Total users: ", value=len(self.client.users), inline=False)
        embed.add_field(name="Total channels: ", value=sum(1 for g in self.client.guilds for _ in g.channels), inline=False)
        cached = sum(1 for m in self.client.cached_messages)
        if cached == 1000:
            cached = "Max"
        embed.add_field(name="Number of cached messages: ", value=cached, inline = False)
        embed.add_field(name="Support server: ", value="https://discord.gg/DxCvp627AT", inline=False)
        embed.add_field(name="Github: ", value="https://github.com/Cinnamon1212/CyberSecDiscordBot", inline=False)
        embed.add_field(name="OS: ", value=platform.platform(), inline=False)
        process = psutil.Process(os.getpid())
        embed.add_field(name="Memory usage: ", value=f"{round(process.memory_info().rss / 1024 ** 2, 2)} Mbs", inline=False)
        embed.add_field(name="CPU usage:", value=f"{process.cpu_percent(interval=None)}%", inline=False)
        embed.add_field(name="Python version: ", value=sys.version, inline=False)
        embed.add_field(name="Discord.py version: ", value=discord.__version__)
        embed.add_field(name="Tor version", value=torversion, inline=False)
        mtime = ctx.message.created_at
        embed.set_footer(text=f"Asked by {ctx.author.name} " + mtime.strftime("%d/%m/%y %X"))
        await ctx.send(embed=embed)

    @commands.command(name="invite", description="invite the bot to your server")
    async def invite(self, ctx):
        embed = Embed(title="Bot invites", colour=discord.Colour.random())
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.add_field(name="Invite the bot to your server: ", value="https://bit.ly/3fGmftl", inline=False)
        embed.add_field(name="Join the support server: ", value="https://discord.gg/DxCvp627AT", inline=False)
        dtime = ctx.message.created_at
        embed.set_footer(text=f"Asked by {ctx.author.name} " + dtime.strftime("%d/%m/%y %X"))
        await ctx.send(embed=embed)

    @commands.command(name="vote", description="Vote for the bot on top.gg", aliases=["top.gg", "topgg"])
    async def vote(self, ctx):
        embed = Embed(title="All votes are appreciated!", colour=discord.Colour.random())
        embed.add_field(name="Top.gg", value="[vote](https://top.gg/bot/766312320589627463/vote)")
        dtime = ctx.message.created_at
        embed.set_footer(text=f"Asked by {ctx.author.name} " + dtime.strftime("%d/%m/%y %X"))
        await ctx.send(embed=embed)

    @commands.command(name="donate", description="Make a bitcoin/patreon donation", aliases=["donation"])
    async def donate(self, ctx):
        embed = Embed(title="All donations are appreciated :)")
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.add_field(name="Patreon: ", value="[Link](https://www.patreon.com/cinnamon1212)", inline=False)
        embed.add_field(name="Bitcoin: ", value="bc1q9ery77lperksj6fc0thedp5vkj33vfsqx8880xu3t44r3hexnsfshlzve0", inline=False)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(misc(client))
