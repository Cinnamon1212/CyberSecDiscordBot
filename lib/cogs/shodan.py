import discord, shodan, json, socket
from discord.ext import commands
from discord import Embed, Colour
from pygicord import Paginator
from aiohttp import request

with open('secrets.json', 'r') as secrets:
    data = secrets.read()
shodanapikey = json.loads(data)
apikey = shodanapikey['shodankey']
api = shodan.Shodan(apikey)

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

    @commands.command(name="searchshodan", description="Search shodan's API for a query", aliases=["shodansearch"])
    async def searchshodan(self, ctx, *, query=None):
        text = "Usage: ./searchshodan [query]"
        if query is None:
            await ctx.send(f"```{text}```")
        else:
            async with request("GET", f"https://api.shodan.io/shodan/host/search?key={apikey}&query={query}&pages=1&minify=True") as r:
                data = await r.json()
            pages = []
            if len(data['matches']) > 5:
                matches = data['matches'][0:5]
            else:
                matches = data['matches']
            embed = Embed(title=f"Search results for {query}", colour=discord.Colour.red(), inline=False)
            embed.add_field(name="Number of results: ", value=data['total'], inline=False)
            try:
                embed.add_field(name="Scroll ID: ", value=data['_scroll_id'], inline=False)
            except KeyError:
                pass
            pages.append(embed)
            x = 1
            for match in matches:
                embed = Embed(title=f"Result #{x}", colour=discord.Colour.red())
                try:
                    ip_addr = match['host']
                except KeyError:
                    try:
                        ip_addr = match['ip_str']
                    except KeyError:
                        ip_addr = None

                if ip_addr is not None:
                    embed.add_field(name="IP Address: ", value=ip_addr, inline=False)

                if match['os'] is not None:
                    embed.add_field(name="OS: ", value=match['os'], inline=False)
                try:
                    embed.add_field(name="Port: ", value=match['port'], inline=False)
                except KeyError:
                    pass

                try:
                    embed.add_field(name="Transport: ", value=match['transport'])
                except KeyError:
                    pass

                try:
                    embed.add_field(name="Organization: ", value=match['org'], inline=False)
                except KeyError:
                    pass
                location = ""
                try:
                    location += f"{match['location']['country_name']}\n"
                except KeyError:
                    pass

                try:
                    location += f"{match['location']['longitude']}, {match['location']['latitude']}\n"
                except KeyError:
                    location = None

                if location is not None:
                    embed.add_field(name="Location: ", value=location, inline=False)
                try:
                    embed.add_field(name="ISP: ", value=match['isp'], inline=False)
                except KeyError:
                    pass

                try:
                    domain_names = ""
                    for domain in match['domains']:
                        domain_names += f"{domain}\n"
                    embed.add_field(name="Domains: ", value=domain_names, inline=False)
                except KeyError:
                    pass
                try:
                    cves = match['vulns'].keys()
                    cve_str = ""
                    for cve in cves:
                        cve_str += f"{cve}\n"
                except KeyError:
                    pass

                try:
                    embed.add_field(name="ASN: ", value=match['asn'], inline=False)
                except KeyError:
                    pass

                x += 1
                pages.append(embed)
            paginator = Paginator(pages=pages)
            await paginator.start(ctx)







def setup(client):
    client.add_cog(shodan(client))
