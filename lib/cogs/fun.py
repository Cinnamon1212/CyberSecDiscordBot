import discord, random, re, json, lyricsgenius
from discord import Embed
from discord.ext import commands
from aiohttp import request

with open('secrets.json', 'r') as secrets:
    data = secrets.read()
secrets = json.loads(data)
geniustoken = secrets['genius']

def clean_string(string):
    string = re.sub('@', '@\u200b', string)
    string = re.sub('#', '#\u200b', string)
    return string

class fun(commands.Cog):
    def __init__(self, client):
        self.client = client

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

    @eightball.error
    async def _8b_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a question")
        else:
            raise

    @commands.command(name="randomnumber", aliases=['rnum', 'randomnum', 'random'], description="Chooses a random number between two values")
    async def randomnumber(self, ctx, num1, num2):
        if int(num1) and int(num2) >= 1:
            numval = random.randrange(int(num1), int(num2))
            await ctx.send(f'The random number is {numval}')
        elif int(num1) == int(num2):
            await ctx.send('Please enter two different numbers')
        else:
            await ctx.send('Please enter a whole number above 0')

    @randomnumber.error
    async def rnum_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a question")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please enter two integers")
        else:
            raise

    @commands.command(name="slap", description="Slaps a player of your choice!")
    async def slap(self, ctx, member: discord.Member, *, reason='no reason'):

        memberid = member.id
        memberexists = ctx.guild.get_member(memberid)
        if memberexists is None:
            await ctx.send("This user does not exist in the server!")
        else:
            await ctx.send(f"{member.mention} was slapped for {reason}")

    @slap.error
    async def slap_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a member")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("Discord member does not exist!")
        else:
            raise

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

    @commands.command(name="animalfact", aliases=["animalfacts"],description="Random animal facts!")

    async def animal_fact(self, ctx, animal: str):
        """ Available animals: Dog, cat, panda, fox, bird and koala. """
        animal = animal.lower()
        if animal in ("dog", "cat", "panda", "fox", "bird", "koala"):
            URL = f"https://some-random-api.ml/facts/{animal}"
            image_link = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"
            async with request("GET", image_link, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    image_link = data["link"]
                else:
                    image = None
            async with request("GET", URL, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    embed = Embed(title=f"{animal.title()} fact",
                                  description=data["fact"],
                                  colour=ctx.author.colour)
                    embed.set_footer(text=f"Asked by {ctx.author.name}")
                    if image_link is not None:
                        embed.set_image(url=image_link)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"API returned {response.status}")
        else:
            await ctx.send("No facts available for provided animal")

    @animal_fact.error
    async def animalfact_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Please enter a string")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter an animal out of: Dog, cat, panda, fox, bird and koala. ")

    @commands.command("lyrics", description="Searches genius for song lyrics", aliases=["genius"])
    async def lyrics(self, ctx, *, song: str):
        genius = lyricsgenius.Genius(geniustoken)
        song = genius.search_song(song)
        try:
            if len(song.lyrics) < 2000:
                await ctx.send(f"```{song.lyrics}```")
            else:
                filename = f"{song.id}_{ctx.author.id}.txt"
                with open(filename, "x") as f:
                    f.writelines(song.lyrics)
                f.close()
                await ctx.send("Here are the song lyrics: ")
                await ctx.send(file=discord.File(filename))
                os.remove(filename)
        except HTTPError as e:
            await ctx.send(f"Unable to fetch lyrics for {song}")
            print(e.errno)
            print(e.args[0])
            print(e.args[1])
        except AttributeError as e:
            print(e)
            await ctx.send(f"Could not fetch lyrics for {song}")
        except Timeout:
            await ctx.send("Lyrics command timed out")


    @lyrics.error
    async def lyrics_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a song name")
        else:
            print(error)

def setup(client):
    client.add_cog(fun(client))
