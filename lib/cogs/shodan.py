import discord,shodan, json
from discord.ext import commands
from discord import Embed, Colour
api = shodan.Shodan('Nope')


class shodan(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.command(name="shodanlookup", description="Looks up an IP using the shodan API")
    async def shodan(self, ctx, ip):
        info = api.host(ip)
        embed = Embed(title=f"Information for {ip}",
                      colour=discord.Colour.red(),
                      inline=False)
        if info['os'] is None:
            embed.add_field(name="Operating system:", value="OS cannot be identified")
        else:
            embed.add_field(name="Operating system:", value=str(info['os']))
        embed.add_field(name="ports: ", value=str(info['ports']))
        embed.add_field(name="Hostnames: ", value=str(info['hostnames']))
        embed.add_field(name="Domains: ", value=str(info['domains']))
        embed.add_field(name="ISP: ", value=str(info['isp']))
        embed.add_field(name="Country: ", value=str(info['country_name']))
        await ctx.send(embed=embed)
    

    # Requires paid shodan
    #@commands.command(name="shodansearch", description="Searches through shodan")
    #async def shodansearch(self, ctx, *, query):
    #    embed = Embed(name=f"Shodan search for {query}",
    #                  description="showing the top results:")

    #    for banner in api.search_cursor(f'http.title:"{query}"'):
    #        resultnumber = 1
    #        embed.add_field(name="Result:", value=banner)
    #        resultnumber += 1
    #    await ctx.send(embed=embed)



def setup(client):
    client.add_cog(shodan(client))
