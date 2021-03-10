import discord
import praw
import random
import os
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

    @commands.command(name="rule34", aliases=['nsfw', 'r34'], description="Random post from the rule34 subreddit")
    async def rule34(self, ctx):
        if ctx.channel.is_nsfw():
            subreddit = reddit.subreddit("rule34")
            all_subs = []

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
        else:
            await ctx.send("Please use this command in an NSFW channel")

    @commands.command(name="minecraft", aliases=['mc'], description="Random post from the minecraft subreddit")
    async def minecraft(self, ctx):
        subreddit = reddit.subreddit("minecraft")
        all_subs = []

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

    @commands.command(name="searchreddit", aliases=['rsearch', 'redsearch'], description="Returns random post from a given subreddit")
    async def searchreddit(self, ctx, usergivensub):
        usergivensub = str(usergivensub)
        subreddit = reddit.subreddit(usergivensub)
        all_subs = []
        if subreddit.over18:
            if ctx.channel.is_nsfw():
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


def setup(client):
    client.add_cog(reddit_commands(client))
