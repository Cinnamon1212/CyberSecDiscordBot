import discord, os, requests
from aiohttp import request
from discord import Embed, colour
from discord.ext import commands
class networkingtools(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="iplookup", description="Provides geoinformation on an IP", aliases=["geoip", "ip", "ipinfo"])
    async def nmap(self, ctx, ip=""):
        if ip == "":
            await ctx.send("Please provide an IP")
        else:
            url = "http://ip-api.com/json/" + ip
            async with request("GET", url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    if data['status'] == "success":
                        embed = Embed(title=f"Information for {ip}",
                                      colour=discord.Colour.red(),
                                      inline=False)
                        embed.set_thumbnail(url="https://www.omnivisiondesign.com/wp-content/uploads/2013/06/IP_address.jpg")
                        embed.add_field(name="Country: ", value=data['country'])
                        embed.add_field(name="Country code: ", value=data['countryCode'])
                        embed.add_field(name="Region: ", value=data['regionName'])
                        embed.add_field(name="City: ", value=data['city'])
                        embed.add_field(name="Organisation: ", value=data['org'])
                        embed.add_field(name="ISP: ", value=data['isp'])
                        time = ctx.message.created_at
                        embed.set_footer(text=f"Asked by {ctx.author.name} " + time.strftime("%x%X"))
                        await ctx.send(embed=embed)
                elif response.status == 429:
                    await ctx.send("Daily iplookup limit reached")
                else:
                    await ctx.send("There was an issue with the API, please try again later!")
                    print(f" API returned {response.status}")
def setup(client):
    client.add_cog(networkingtools(client))
