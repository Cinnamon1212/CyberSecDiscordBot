import discord
import praw
import random
import os
import json
from discord.ext import commands
from discord import Embed


reddit = praw.Reddit(client_id="mJfUbgRdBTcR6A",
                     client_secret="78eg7HF1H9Ie1uD7NjGidsCgPNh2tg",
                     username="C1nn4m0nGinger",
                     password="T22N9mf6hXHYmhC",
                     user_agent="pythonbot")



class reddit_commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="codingmemes", description="Random coding meme from the coding meme subreddit", aliases=["codememe"])
    async def codingmemes(self, ctx):
        subreddit = reddit.subreddit('codingmemes')
        all_subs = []
        top = subreddit.top(limit=50)

        for submission in top:
            all_subs.append(submission)
        random_sub = random.choice(all_subs)
        embed = discord.Embed(title=submission.name, colour=discord.Colour.random())
        embed.set_image(submission.url)
        embed.set_footer(text=f"Asked by {ctx.author.name}")
        await ctx.send(embed=embed)
    @commands.command(name="searchreddit", aliases=['rsearch', 'redsearch'], description="Returns random post from a given subreddit")
    async def searchreddit(self, ctx, *, usergivensub: str):
        try:
            subreddit = reddit.subreddit(usergivensub)
            sub_exists = True
        except NotFound:
            await ctx.send(f"Unable to find {subreddit}")
        if sub_exists == True:
            all_subs = []
            if subreddit.over18:
                if ctx.channel.is_nsfw():
                    top = subreddit.top(limit=50)

                    for submission in top:
                        all_subs.append(submission)
                    random_sub = random.choice(all_subs)
                    name = random_sub.title
                    url = random_sub.url

                    embed = discord.Embed(title=name, colour=discord.Colour.gold())
                    embed.set_image(url=url)
                    embed.set_footer(text=f"Asked by {ctx.author.name}")
                    await ctx.send(embed=embed)

                else:
                    await ctx.send("Please use this command in an NSFW channel")
            else:
                top = subreddit.top(limit=50)

                for submission in top:
                    all_subs.append(submission)

                random_sub = random.choice(all_subs)
                name = random_sub.title
                url = random_sub.url
                embed = discord.Embed(title=name, color=discord.Color.gold())
                embed.set_image(url=url)
                embed.set_footer(text=f"Asked by {ctx.author.name}")
                await ctx.send(embed=embed)

    @searchreddit.error
    async def rsearch_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("There was an error while fetching the subreddit")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter the subreddit name!")
        else:
            raise

def setup(client):
    client.add_cog(reddit_commands(client))
