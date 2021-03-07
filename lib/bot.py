import discord, os
from discord.ext import commands
from discord.ext.commands import CommandNotFound
client = commands.Bot(command_prefix='./', case_insensitive=True,
                      intents=discord.Intents.all())
token = open("token0.txt", "r")


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
client.run(token.readline(), reconnect=True)


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
        await ctx.send("No such command, please use ./help")
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
