import discord, requests, os, dateutil.parser
from discord.ext import commands
from discord import Embed, Colour
from aiohttp import request

class covid(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="covid19", description="Gives information on covid19 by country code, example: France = FR")
    async def covid19(self, ctx, query=""):
        if query == "":
            url = "http://api.coronatracker.com/v3/stats/worldometer/global"

            async with request("GET", url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    d = dateutil.parser.parse(data['created'])
                    embed = Embed(title="Global numbers: ",
                                  colour=discord.Colour.green(),
                                  inline=False)
                    embed.set_thumbnail(url="https://www.pathway.org.uk/wp-content/uploads/covid19.jpeg")
                    embed.add_field(name="Total cases: ", value=f"{str(data['totalConfirmed'])} cases")
                    embed.add_field(name="Total deaths: ", value=f"{str(data['totalDeaths'])} deaths")
                    embed.add_field(name="Total recovered:", value=f"{str(data['totalRecovered'])} recovered")
                    embed.set_footer(text=f"{d}")
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("There was an issue with the API, please try again later!")
                    print(f"Api returned{response.status}")
        else:
            url = "https://api.coronatracker.com/v3/stats/worldometer/country?countryCode=" + query
            async with request("GET", url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    d = dateutil.parser.parse(data[0]['lastUpdated'])

                    embed = Embed(title=f"{data[0]['country']} numbers: ",
                                  colour=discord.Colour.green(),
                                  inline=False)
                    embed.set_thumbnail(url="https://www.dandc.eu/sites/default/files/styles/article_stage/public/covid-dossier-symbolbild-131029709_1.jpg?itok=oWcCZkOThttps://www.dandc.eu/en/briefings/coronavirus-pandemic-affecting-societies-and-economies-around-globe")
                    embed.add_field(name="Total confirmed: ", value=f"{data[0]['totalConfirmed']}")
                    embed.add_field(name="Total deaths: ", value=f"{data[0]['totalDeaths']}")
                    embed.add_field(name="Total recovered: ", value=f"{data[0]['totalRecovered']}")
                    embed.add_field(name="Total critical", value=f"{data[0]['totalCritical']}")
                    embed.add_field(name="Total confirmed per million", value=f"{data[0]['totalConfirmedPerMillionPopulation']}")
                    embed.set_footer(text=f"{d}")
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("There was an issue with the API, please try again later!")
                    print(f" API returned {response.status}")
def setup(client):
    client.add_cog(covid(client))
