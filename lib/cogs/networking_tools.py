import discord, os, requests, string, passgen, subprocess, socket, json, time, aionmap, re, asyncio
from socket import gaierror
from datetime import datetime
from discord import Embed, colour
from discord.ext import commands
from aiohttp import request

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

def validate_port(s):
    try:
        s = int(s)
    except ValueError:
        return False

    if s <= 65535:
        return True
    else:
        return False

async def ping_f(ip, count):
    args = f"ping -c {count} {ip}"
    cmd = await asyncio.create_subprocess_shell(args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await cmd.communicate()
    output = str(stdout, 'utf-8')
    return output

async def dig_f(ip):
    args = f"dig {ip}"
    cmd = await asyncio.create_subprocess_shell(args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await cmd.communicate()
    output = str(stdout, 'utf-8')
    return output

async def payloadgen(ctx, payload, ip, port):
    print(ctx.author.id)
    args = f"msfvenom -p {payload} LHOST={ip} LPORT={port} -o ./payloads/{ctx.author.id}_payload.txt"
    cmd = await asyncio.create_subprocess_shell(args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await cmd.communicate()

async def nmap_scan(scantype, ip, ports=""):
    scanner = aionmap.PortScanner()
    if ports != "":
        if "," not in ports:
            ports = re.sub("\s+", ",", ports.strip())
        result = await scanner.scan(ip, ports, scantype, sudo=False)
        return result
    else:
        result = await scanner.scan(ip, None, scantype, sudo=False)
        return result

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

    @commands.command(name="dig", description="Dig comamnd, takes a domain or IP")
    async def dig(self, ctx, DNS=""):
        text = "Usage: ./dig [DNS]"
        if DNS == "":
            await ctx.send(f"```{text}```")
        else:
            try:
                ip = socket.gethostbyname(DNS)
                check = True
            except gaierror:
                await ctx.send(f"```Unable to associate address to DNS\n{text}```")
                check = False
            if check is True:
                if validate_ip(ip) is True:
                    output = await dig_f(DNS)
                    await ctx.send(f"```\n{output}```")
                elif validate_ip(DNS) is False:
                    await ctx.send(f"```Invalid host provided\n{text}```")
                else:
                    await ctx.send(f"```Unable to validate DNS\n{text}```")

    @commands.command(name="passgen", description="generates a number of passwords with a given length", aliases=["passwordgenerator", "password"])
    async def passwords(self, ctx, length: int, number=1):
        text = "Usage: ./passgen [length] (number)"
        if number <= 25 and number >= 1:
            if length <= 25 and length >= 4:
                embed = Embed(title="Passwords ",
                              description=f"{number} passwords of {length} length",
                              colour=discord.Colour.random())
                i = 0
                num = 0
                passwords = set({})
                while i != number:
                    output = passgen.passgen(length=length, punctuation=True, digits=True, letters=True, case='both')
                    passwords.add(output)
                    i += 1
                for password in passwords:
                    embed.add_field(name=f"Password {num + 1}", value=password, inline=False)
                    num += 1
                time = ctx.message.created_at
                embed.set_footer(text=f"Asked by {ctx.author.name} " + time.strftime("%d/%m/%y %X"))
                await ctx.author.send(embed=embed)
                await ctx.send("Passwords were send to your DMs!")
            else:
                await ctx.send(f"```Length must be between 4 and 25\n{text}```")
        else:
            await ctx.send(f"```You must have between 1 and 25 passwords\n{text}```")

    @passwords.error
    async def passgen_error(self, ctx, error):
        text = "Usage: ./passgen [amount] [length]"
        if isinstance(error, commands.BadArgument):
            await ctx.send(f"```Invalid number of passwords or length\n{text}```")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter the number of passwords and the length")
        else:
            raise

    @commands.command(name="ping", description="Pings any provided IP")
    async def ping(self, ctx, ip: str = "", count: int = 3):
        text = "Usage: ./ping {ip} {count}\nMax count is 10"
        ip = socket.gethostbyname(ip)
        if validate_ip(ip) is True:
            if count <= 10:
                output = await ping_f(ip, count)
                await ctx.send(f"```{output}```")
            else:
                await ctx.send(f"```You may only have up to 10 ping requests\n{text}```")
        else:
            await ctx.send(f"```Please enter a valid IP address\n{text}```")




    @commands.command(name="nmap", description="Performs basic scans using the nmap. The bot will be paused while this runs! ")
    @commands.cooldown(2, 30, commands.BucketType.user)
    async def nmapscan(self, ctx, scantype: str, ip=None, *, ports=""):
        text = "Usage: ./nmap [scantype] [ip] (port)\nAvailable scan types: -sT, -sV"
        scan_types = ['-PS', '-sT', '-sV']
        if scantype in scan_types:
            ip = socket.gethostbyname(ip)
            if validate_ip(ip) is True:
                if ports != "":
                    if "," in ports:
                        a = ports.split(",")
                    else:
                        a = ports.split()
                    for port in a:
                        if validate_port(port):
                            validports = True
                    if validports is True:
                        checks = True
                    else:
                        checks = False
                        await ctx.send(f"```Invalid ports selected!\n{text}```")
                else:
                    checks = True
            else:
                checks = False
                await ctx.send(f"```{text}```")
        else:
            await ctx.send(f"```{text}```")
            checks = False

        if checks is True:
            scan_start = datetime.now()
            if ports != "":
                await ctx.send(f"Executing: nmap {scantype} {ip} -p {ports}, results will be sent to your DMs!")
                results = await nmap_scan(scantype, ip, ports)
            else:
                await ctx.send(f"Executing: nmap {scantype} {ip}, results will be sent to your DMs!")
                results = await nmap_scan(scantype, ip)
            if isinstance(results, Exception):
                await ctx.author.send(f"The bot encountered an error while trying to scan {ip}!")
            else:
                x = results.get_raw_data()
                scaninfo = x['_scaninfo']
                stats = x['_runstats']
                finish = stats['finished']
                host = x['_hosts']
                hoststats = stats['hosts']
                strtosend = f"""
Scan started at: {results.startedstr}
Nmap version: {results.version}
{host[0]} (Total up: {hoststats['total']})

Scan info:
    Type: {scaninfo['type'].upper()}

    Protocol: {scaninfo['protocol'].upper()}

Total number of services {scaninfo['numservices']}

services: \n{scaninfo['services']}

Finish time: {finish['timestr']} (Elapsed: {finish['elapsed']})
Requested by: {ctx.author.name}
                """
                filename = f"./scans/{results.started}_{ctx.author.id}.txt"
                with open(filename, 'a') as f:
                    f.write(strtosend)
                f.close()
                await ctx.author.send(file=discord.File(filename))
                os.remove(filename)

    @nmapscan.error
    async def scan_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("```Usage: ./nmap [scantype] [ip] (port)```")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"The nmap command is on cooldown, please try again in: {error.retry_after:.2f}s")
        else:
            raise

    @commands.command(name="msfvenom", description="Geneate msf payload, for payloads type ./msfvenom", aliases=["msfpayload"])
    async def msfvenom(self, ctx, payload=None, ip=None, port=None):

        text = "Usage: ./msfvenom [payload] [ip] [port]"
        if payload is None:
            await ctx.send(f"```{text}```")
        else:
            if validate_port(port) is True:
                if validate_ip(ip) is True:
                    port = int(port)
                    bad_chars = [';', ':', '!', '*', '#', '$', '(', ')']
                    payload = ''.join((filter(lambda i: i not in bad_chars, payload)))
                    payload = payload.lower()
                    await ctx.send(f"Generating {payload}")
                    await payloadgen(ctx, payload, ip, port)
                    await ctx.author.send(file=discord.File(f"./payloads/{ctx.author.id}_payload.txt"))
                    os.remove(f"./payloads/{ctx.author.id}_payload.txt")
                else:
                    await ctx.send(f"```Please enter a valid IP\n{text}```")
            else:
                await ctx.send(f"```Please enter a valid port\n{text}```")
    @commands.command(name="cvesearch", description="Search", alises=["cveid", "cvelookup"])
    async def cvesearch(self, ctx, cveid):
        if cveid == "":
            await ctx.send("Please provide a cve ID")
        else:
            url = "https://cve.circl.lu/api/cve/" + cveid
            async with request("GET", url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    embed = Embed(title=f"Info on {cveid}",
                                  description=f"Name: {data['capec'][0]['name']}",
                                  colour=discord.Colour.random(),
                                  inline=True)
                    embed.add_field(name="Authentication: ", value=data['access']['authentication'], inline=True)
                    embed.add_field(name="Complexity: ", value=data['access']['complexity'], inline=True)
                    embed.add_field(name="Vector: ", value=data['access']['vector'], inline=True)
                    embed.add_field(name="Summary: ", value=data['capec'][0]['summary'], inline=True)
                    embed.add_field(name="Solutions: ", value=data['capec'][0]['solutions'], inline=True)

                    time = ctx.message.created_at
                    embed.set_footer(text=f"Asked by {ctx.author.name} " + time.strftime("%d/%m/%y %X"))

                    await ctx.send(embed=embed)
    @cvesearch.error
    async def cves_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a CVE to search")
        else:
            raise

def setup(client):
    client.add_cog(networkingtools(client))
