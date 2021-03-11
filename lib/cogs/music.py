import discord, youtube_dl, os, asyncio, datetime
from discord.utils import get
from discord.ext import commands
from discord import Embed, colour

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
        self.duration = data.get('duration')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="play", description="Plays a song from a URL")
    async def play(self, ctx, url: str):
        if ctx.voice_client is not None:
            channel = ctx.author.voice.channel
            return await ctx.voice_client.move_to(channel)
        else:
            channel = ctx.author.voice.channel
            await channel.connect()
            player = await YTDLSource.from_url(url, loop=self.client.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
            embed = Embed(title="Playing: ")
            embed.add_field(name=player.title, value=str(datetime.timedelta(seconds=player.duration)))
            await ctx.send(embed=embed)

    @commands.command(name="leave", description="Disconnects the bot from the channel")
    async def leave(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice is not None:
            await voice.disconnect()
        else:
            await ctx.send("Bot is currently not connected to a channel")

    @commands.command(name="pause", description="pauses the music currently playing")
    async def pause(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("There is nothing currently playing")

    @commands.command(name="resume", description="Resumes music")
    async def resume(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if not voice.is_playing():
            voice.resume()
        else:
            await ctx.send("The bot is not paused")

    @commands.command(name="stop", description="Stops the music")
    async def stop(self, ctx):
        await ctx.voice_client.disconnect()

def setup(client):
    client.add_cog(music(client))
