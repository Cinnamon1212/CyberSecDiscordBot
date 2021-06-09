import discord, os, json
from discord.ext import commands
from discord.ext.commands import CommandNotFound
intents = discord.Intents.default()


client = commands.Bot(command_prefix='.//', case_insensitive=True,
                      intents=intents)

with open('secrets.json', 'r') as secrets:
    data = secrets.read()
tokendata = json.loads(data)
token = tokendata['token']


# Owner commands
@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.command()
@commands.is_owner()
async def ShowServers(ctx):
    servers = client.guilds
    names = []
    for guild in servers:
        names.append([guild.name, guild.member_count])
    text = """
----------------
Server: members
----------------
"""
    for name in names:
        text += f"{name[0]}: {name[1]}\n"
    await ctx.send(f"```{text}```")
@client.command()
@commands.is_owner()
async def remote_shutdown(ctx):
    await ctx.send("Shutting down!")
    await client.close()

@client.command()
@commands.is_owner()
async def changestatus(ctx, status, *, game):
    if status == "online":
        await client.change_presence(status=discord.Status.online, activity=discord.Game(game))
    elif status == "idle":
        await client.change_presence(status=discord.Status.idle, activity=discord.Game(game))
    elif status == "dnd":
        await client.change_presence(status=discord.Status.dnd, activity=discord.Game(game))
    elif status == "invis":
        await client.change_presence(status=discord.Status.invisible, activity=discord.Game(game))
    else:
        await ctx.send("Invalid status")

async def shutdown(self):
    print("Closing connection to Discord...")

    await super().close()


async def close(self):
    print("Closing on keyboard interrupt...")
    await self.shutdown()


async def on_connect(self):
    print(f" Connected to Discord (latency: {self.latency*1000:,.0f} ms).")


async def on_resumed(self):
    print("Bot resumed.")


async def on_disconnect(self):
    print("Bot disconnected.")


async def on_error(self, err, *args, **kwargs):
    if err == "on_command_error":
        await args[0].send("Something went wrong")
    raise


async def on_command_error(self, ctx, exc):
    if isinstance(exc, CommandNotFound):
        pass
    elif hasattr(exc, "original"):
        raise exc.original
    else:
        raise exc


async def on_ready(self):
    self.client_id = (await self.application_info()).id
    print("Bot ready.")

async def process_commands(self, msg):
    ctx = await self.get_context(msg, cls=commands.Context)

    if ctx.command is not None:
        await self.invoke(ctx)

async def on_message(self, msg):
    if not msg.author.bot:
        await self.process_commands(msg)

client.run(token, reconnect=True)
