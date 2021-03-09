import discord, os, requests, json
from bs4 import BeautifulSoup
from discord.ext import commands
from discord import Embed
from aiohttp import request
from googleapiclient.discovery import build

with open('secrets.json', 'r') as secrets:
    data = secrets.read()
googleapikey = json.loads(data)
apikey = googleapikey['googleapi']



class googleapi(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="youtube", description="Searches youtube using the Youtube V3 API", aliases=["YT", "YSearch"])
    async def youtube(self, ctx, query):
        youtube = build('youtube', 'v3', developerKey=apikey)
        search_response = youtube.search().list(
            q=query,
            part='id, snippet',
            maxResults=10
        ).execute()
        videos = []
        num = 1
        embed = Embed(title=f"Search results for {query}",
                      colour=discord.Colour.random(),
                      inline=False)
        for search_result in search_response.get('items', []):
            if search_result['id']['kind'] == 'youtube#video':
                videos.append(f"\n{search_result['snippet']['title']} [Link](https://youtu.be/{search_result['id']['videoId']})\n")
            else:
                pass
        for video in videos:
            video = BeautifulSoup(video)
            embed.add_field(name=f"Result #{num}", value=f"{video}")
            num += 1
        await ctx.send(embed=embed)

    @youtube.error
    async def youtube_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter something to search")
        else:
            raise

def setup(client):
    client.add_cog(googleapi(client))
