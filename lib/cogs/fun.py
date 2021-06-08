import discord, aiofiles, random, re
from discord.ext import commands
from discord import Embed

def GetFacts():
    with open('uselessfacts.txt', 'r') as facts:
        uselessfacts = facts.read()
    uselessfacts = uselessfacts.split("\n")
    return uselessfacts

def GetLinuxJokes():
    with open("linuxjokes.txt") as jokes:
        linux_jokes = jokes.read()
    linux_jokes = linux_jokes.split("\n")
    return linux_jokes

def clean_string(string):
    string = re.sub('@', '@\u200b', string)
    string = re.sub('#', '#\u200b', string)
    return string


class fun(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.uselessfacts = GetFacts()
        self.linux_jokes = GetLinuxJokes()


    @commands.command(name="echo", aliases=['say'], description="echoes message to a specified channel")
    async def echo(self, ctx, destination: discord.TextChannel = None, *, msg: str):
        if not destination.permissions_for(ctx.author).send_messages:
            return await ctx.message.add_reaction("\N{WARNING SIGN}")
        msg = clean_string(msg)
        destination = ctx.message.channel if destination is None else destination
        embed = Embed(title=f"{ctx.author.name} says: ",
                      colour=ctx.author.colour)
        embed.add_field(name=msg, value="⠀")
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await destination.send(embed=embed)
        return await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")

    @echo.error
    async def echo_error(self, ctx, error):
        if isinstance(error, commands.ChannelNotFound):
            await ctx.send("Please enter an existing channel")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please provide a channel and message")
        else:
            raise

    @commands.command(name="eightball", aliases=['8B', '8ball'], description="A magic 8 ball command!")
    async def eightball(self, ctx, *, question):
            """ Ask the magic 8ball a question """
            responses = ['It is decidedly so.',
                         'Without a doubt.',
                         'Yes, definitely.',
                         'As I see it, yes.',
                         'Most likely.',
                         'Signs point to yes.',
                         'Reply hazy, try again.',
                         'Ask again, later.',
                         'Better not tell you now.',
                         'Cannot predict now.',
                         'Concentrate and ask again.',
                         'Do not count on it.',
                         'My reply is no.',
                         'My sources say no.',
                         'Outlook not so good.',
                         'I doubt it.']
            await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')
            await ctx.send(f"```{random.choice(responses)}```")

    @eightball.error
    async def _8b_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a question")
        else:
            raise

    @commands.command(name="uselessfact", aliases=["useless", "randomfact"], description="Ramdom fact")
    async def useless_fact(self, ctx):
        fact = random.choice(self.uselessfacts)
        await ctx.send(f"```{fact}```")

    @commands.command(name="linuxjoke", description="Random Linux joke", aliases=["ljoke"])
    async def linuxjokes(self, ctx):
        joke = random.choice(self.linux_jokes)
        joke = joke.split("¦")
        await ctx.send(f"```{joke[0].strip()}\n{joke[1].strip()}```")

def setup(client):
    client.add_cog(fun(client))
