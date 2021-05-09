import discord, shodan, json, socket
from discord.ext import commands
from discord import Embed, Colour

with open('secrets.json', 'r') as secrets:
    data = secrets.read()
shodanapikey = json.loads(data)
apikey = shodanapikey['shodankey']
api = shodan.Shodan(apikey)


def validate_ip(s):
    if s is not None:
        restricted = ["192.16", "173.16", "172.31", "127.0."]
        a = s.split('.')
        if len(a) != 4:
            return False
        for x in a:
            if not x.isdigit():
                return False
            i = int(x)
            if i < 0 or i > 255:
                return False
        firstsix = s[0:6]
        print(firstsix)
        check = any(r in firstsix for r in restricted)
        print(check)
        if check is True:
            return False
        else:
            if s[2] == "10":
                return False
            else:
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
        text = "Usage: ./shodanlookup [IP]"
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"```Please provide an IP\n{text}```")
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"```Please ensure you provide an IP\{text}```")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"```The API could not check that IP\n{text}```")
        else:
            raise

def setup(client):
    client.add_cog(shodan(client))
