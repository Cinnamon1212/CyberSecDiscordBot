import discord, shodan, json, subprocess, string, socket
from discord.ext import commands
from discord import Embed, Colour

with open('secrets.json', 'r') as secrets:
    data = secrets.read()
shodanapikey = json.loads(data)
apikey = shodanapikey['shodankey']
api = shodan.Shodan(apikey)

def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True

class shodan(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.command(name="shodanlookup", description="Looks up an IP using the shodan API")
    async def shodanlookup(self, ctx, ip):
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
        time = ctx.message.created_at
        embed.set_footer(text=f"Asked by {ctx.author.name} " + time.strftime("%d/%m/%y %X"))
        await ctx.send(embed=embed)

    @shodanlookup.error
    async def shodanlookup_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please provide an IP")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please ensure you provide an IP")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("The API could not check that IP")
        else:
            raise

    # Requires paid shodan
    # @commands.command(name="shodansearch", description="Searches through shodan")
    # async def shodansearch(self, ctx, *, query):
    #    embed = Embed(name=f"Shodan search for {query}",
    #                  description="showing the top results:")

    #    for banner in api.search_cursor(f'http.title:"{query}"'):
    #        resultnumber = 1
    #        embed.add_field(name="Result:", value=banner)
    #        resultnumber += 1
    #    await ctx.send(embed=embed)

    @commands.command(name="Honeypot", description="Checks if an IP is a honey pot or not")
    async def honeypot(self, ctx, ip: str):
        ip = socket.gethostbyname(ip)
        if validate_ip(ip) is True:
            output = subprocess.getoutput(f"shodan honeyscore {ip} #")
            if ("Usage: shodan") in output:
                await ctx.send("Please ensure you pass the IP")
            elif("Unable to calculate honeyscore") in output:
                await ctx.send("Unable to calculate honeyscore")
            else:
                embed = Embed(title="Shodan Honeypot check",
                              colour=discord.Colour.random(),
                              description=output)
                embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Runny_hunny.jpg/800px-Runny_hunny.jpg")
                time = ctx.message.created_at
                embed.set_footer(text=f"Asked by {ctx.author.name} " + time.strftime("%d/%m/%y %X"))
                await ctx.send(embed=embed)
        else:
            await ctx.send("Please enter a valid IP!")


def setup(client):
    client.add_cog(shodan(client))
