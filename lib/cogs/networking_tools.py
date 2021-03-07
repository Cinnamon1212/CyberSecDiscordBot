import discord, os, requests, string, passgen, platform, subprocess, dns, dns.resolver, socket
from aiohttp import request
from discord import Embed, colour
from discord.ext import commands


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
                        embed.set_footer(text=f"Asked by {ctx.author.name} " + time.strftime("%d/%m/%y %X"))
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("Could not find IP")
                elif response.status == 429:
                    await ctx.send("Daily iplookup limit reached")
                else:
                    await ctx.send("There was an issue with the API, please try again later!")
                    print(f" API returned {response.status}")

    @commands.command(name="DNSLookup", description="DNS Lookup comamnd, takes DNS and reurned A type records", aliases=["DNS", "nameserverlookup"])
    async def DNSLookup(self, ctx, DNS=""):

        if DNS == "":
            await ctx.send("Please enter a nameserver to lookup")
        else:
            result = dns.resolver.query(DNS, 'A')
            ips = set({})
            for ipval in result:
                output = ipval.to_text()
                ips.add(output)
            embed = Embed(title=f"DNS Lookup for {DNS}")
            for ip in ips:
                embed.add_field(name="Result: ", value=ip, inline=True)
            time = ctx.message.created_at
            embed.set_footer(text=f"Asked by {ctx.author.name} " + time.strftime("%d/%m/%y %X"))
            await ctx.send(embed=embed)

    @commands.command(name="passgen", description="generates a number of passwords with a given length", aliases=["passwordgenerator", "password"])
    async def passwords(self, ctx, number: int, length: int):
        if number in range(0, 26) is False or length in range(3, 51) is False:
            await ctx.send("You must have at least 1 password with 4 characters")
        else:

            embed = Embed(title="Passwords ",
                          description=f"{number} passwords of {length} length: ",
                          colour=discord.Colour.random())
            i = 0
            num = 0
            passwords = set({})
            while i != number:
                output = passgen.passgen(length=length, punctuation=True, digits=True, letters=True, case='both')
                passwords.add(output)
                i += 1
            for password in passwords:
                embed.add_field(name=f"Password {num + 1}", value=password)
                num += 1
            time = ctx.message.created_at
            embed.set_footer(text=f"Asked by {ctx.author.name} " + time.strftime("%d/%m/%y %X"))
            await ctx.author.send(embed=embed)
            await ctx.send("Passwords were send to your DMs!")
    @passwords.error
    async def passgen_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Please enter args as integers")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter the number of passwords and the length")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("Please ensure you ask for at least 1 password with at least 4 characters")
        else:
            raise

    @commands.command(name="ping", description="Pings any provided IP")
    async def ping(self, ctx, count: int, ip: str):
        ip = socket.gethostbyname(ip)
        if validate_ip(ip) is True:
            if count <= 10:
                param = '-n' if platform.system().lower() == 'windows' else '-c'
                output = subprocess.getoutput(f"ping {param} {count} {ip} #")
                await ctx.send(f"```{output}```")
            else:
                await ctx.send("You may only have up to 10 ping requests")
        elif validate_ip(ip) is False:
            await ctx.send("Please enter a valid IP address")

        else:
            await ctx.send("Unable to validate IP")

    @ping.error
    async def ping_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter the number of pings and the IP")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please ensure the number of pings is an integer")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("Please ensure you enter a valid IP address!")
        else:
            raise



def setup(client):
    client.add_cog(networkingtools(client))
