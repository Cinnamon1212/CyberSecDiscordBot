import discord, os, requests, passgen, socket, json, time, aionmap, re, asyncio, math, aiofiles
from socket import gaierror
from datetime import datetime
from discord import Embed, colour
from discord.ext import commands
from aiohttp import request
from pygicord import Paginator

def validate_ip(s):
    if s is not None:
        restricted = ["192.16", "173.16", "172.31", "127.0.", "0.0.0."]
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
        check = any(r in firstsix for r in restricted)
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

async def whois_f(domain):
    args = f"whois {domain}"
    cmd = await asyncio.create_subprocess_shell(args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await cmd.communicate()
    output = str(stdout, 'utf-8')
    print(output)
    return output

async def payloadgen(ctx, payload, ip, port):
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
                async with aiofiles.open(filename, 'a') as f:
                    await f.write(strtosend)
                await ctx.author.send(file=discord.File(filename))
                os.remove(filename)

    @nmapscan.error
    async def scan_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("```Usage: ./nmap [scantype] [ip] (port)\nAvailable scan types: -sT, -sV```")
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
                    bad_chars = [';', ':', '!', '*', '#', '$', '(', ')', '&', '\\', '"', '\'']
                    payload = ''.join((filter(lambda i: i not in bad_chars, payload)))
                    payload = payload.lower()
                    await ctx.send(f"Attempting to generate {payload}")
                    await payloadgen(ctx, payload, ip, port)
                    try:
                        await ctx.author.send(file=discord.File(f"./payloads/{ctx.author.id}_payload.txt"))
                    except:
                        await ctx.send("Unable to generate payload, please ensure a valid payload is selected")
                    os.remove(f"./payloads/{ctx.author.id}_payload.txt")
                else:
                    await ctx.send(f"```Please enter a valid IP\n{text}```")
            else:
                await ctx.send(f"```Please enter a valid port\n{text}```")

    @commands.command(name="cvesearch", description="Search CVEs on https://cve.circl.lu/", alises=["cveid", "cvelookup"])
    async def cvesearch(self, ctx, search_type=None, query=""):
        text = """
Usage: ./cvesearch [search type] (query)

CVE Options:
latest - fetch latest CVE # Returns latest CVE
browse - browse vendors (Microsoft) # returns list of vendor products
id - fetch CVE by ID (CVE-2014-0160)
search - search for a CVE (microsoft/office) # Not working, try ./exDB [query]
dbinfo - Returns a list of database updates

CVE info from: https://cve.circl.lu/
        """
        if search_type is None:
            await ctx.send(f"```{text}```")
        else:
            search_type = search_type.lower()
            if query == "":
                if search_type == "dbinfo":
                    async with request("GET", f"https://cve.circl.lu/api/dbInfo", headers={}) as r:
                        if r.status == 200:
                            data = await r.json()
                            embed = Embed(title="Database information", description="https://cve.circl.lu/", colour=discord.Colour.random())
                            embed.add_field(name="Last CAPEC update: ", value=data['capec']['last_update'], inline=False)
                            embed.add_field(name="Last CPE update: ", value=data['cpe']['last_update'], inline=False)
                            embed.add_field(name="Last CPE other update: ", value=data['cpeOther']['last_update'], inline=False)
                            embed.add_field(name="Last CVE update: ", value=data['cves']['last_update'], inline=False)
                            embed.add_field(name="Last CWE update: ", value=data['cwe']['last_update'], inline=False)
                            embed.add_field(name="Last via 4 update: ", value=data['via4']['last_update'], inline=False)
                            await ctx.send(embed=embed)
                        else:
                            await ctx.send(f"```There was an error while fetching database info\n{text}```")
                elif search_type == "latest":
                    async with request("GET", f"https://cve.circl.lu/api/last/1", headers={}) as r:
                        if r.status == 200:
                            data = await r.json()
                            last = data[0]
                            product = last['vulnerable_product']
                            prod_end = math.ceil(len(product)) / 2
                            products = product[0:int(prod_end)]
                            if products == []:
                                products = "N/A"
                            impact = last['impact']
                            access = last['access']
                            ref = last['references']
                            ref = ref[0:3]
                            ref = "\n".join(ref)
                            summary = last['summary']
                            summary = "".join(summary)
                            CVEReport = f"""
CVE {last['id']} ({last['Published']})

Vulnerability score: {last['cvss']}
Impact:
    Availability: {impact['availability']}
    Confidentiality: {impact['confidentiality']}
    Integrity: {impact['integrity']}

Access:
    Auth: {access['authentication']}
    Complexity: {access['complexity']}
    Vector: {access['vector']}

Product(s):
    {products}

References:
    {ref}

Summary:
{summary} """
                            if len(CVEReport) <= 1994:
                                await ctx.send(f"```{CVEReport}```")
                            else:
                                filename = f"./CVEReports/{ctx.author.id}.txt"
                                async with aiofiles.open(filename, 'a') as f:
                                    await f.write(CVEReport)
                                await ctx.author.send(file=discord.File(filename))
                                os.remove(filename)
                        else:
                            await ctx.send(f"```There was an error while fetching the latest CVEs\n{text}```")
                else:
                    await ctx.send(f"```Please enter a query\n{text}```")
            else:
                if search_type == "browse":
                    async with request("GET", f"https://cve.circl.lu/api/browse/{query}", headers={}) as r:
                        if r.status == 200:
                            data = await r.json()
                        else:
                            data = None
                            await ctx.send(f"```There was an error while browsing for {query}\n{text}```")
                        if data is not None:
                            if 'product' in data:
                                products = data['product']
                                embed = Embed(title=f"Browse results for {query}", colour=discord.Colour.random())
                                x = 1
                                i = 0
                                while i != 25:
                                    try:
                                        z = products[i]
                                        embed.add_field(name=f"Product #{x}", value=z, inline=False)
                                        x += 1
                                        i += 1
                                    except IndexError:
                                        break
                                embed.set_footer(text="CVE results from https://cve.circl.lu/")
                                await ctx.send(embed=embed)
                            else:
                                await ctx.send(f"```Unable to find a result for {query}\n{text}```")
                elif search_type == "id":
                    async with request("GET", f"https://cve.circl.lu/api/cve/{query}", headers={}) as r:
                        if r.status == 200:
                            data = await r.json()
                            pages = []
                            overview = Embed(title=f"CVE Overview: {query}", colour=discord.Colour.random())
                            overview.add_field(name="Last modified: ", value=data['Modified'], inline=False)
                            overview.add_field(name="Published: ", value=data['Published'], inline=False)
                            overview.add_field(name="Assigner: ", value=data['assigner'], inline=False)
                            access = data["access"]
                            overview.add_field(name="Authentication: ", value=access['authentication'], inline=False)
                            overview.add_field(name="Complexity: ", value=access['complexity'], inline=False)
                            overview.add_field(name="Vector: ", value=access['vector'])
                            overview.set_footer(text="CVE results from https://cve.circl.lu/")
                            pages.append(overview)

                            refs = data['references']
                            try:
                                refs = refs[0:10]
                            except IndexError:
                                pass
                            references = Embed(title="References", colour=discord.Colour.random())
                            for r in refs:
                                references.add_field(name="⠀", value=r, inline=False)
                            pages.append(references)

                            capecs = data['capec']
                            try:
                                capecs = capecs[0:3]
                            except IndexError:
                                pass
                            for c in capecs:
                                embed = Embed(title=c['name'], colour=discord.Colour.random())
                                embed.add_field(name="ID: ", value=c['id'], inline=False)
                                embed.add_field(name="Prerequisites", value=c['prerequisites'], inline=False)
                                summary = "".join(c['summary'])
                                embed.add_field(name="Summary: ", value=summary, inline=False)
                                solution = "".join(c['solutions'])
                                embed.add_field(name="Solutions: ", value=solution, inline=False)
                                pages.append(embed)
                            paginator = Paginator(pages=pages)
                            await paginator.start(ctx)
                        else:
                            await ctx.send(f"```There was an error while finding CVE ID: {query}\n{text}```")
                elif search_type == "search":
                    await ctx.send("Not currently working..")
                else:
                    await ctx.send(f"```Invalid search type\n{text}```")

    @commands.command(name="whois", description="perform who is search on a given domain")
    async def whois(self, ctx, domain):
        text = "Usage: ./whois [domain]"
        check = False
        try:
            ip = socket.gethostbyname(domain)
            check = True
        except gaierror:
            await ctx.send(f"Unable to associate IP with the domain\n{text}")
        if check is True:
            if validate_ip(ip) is True:
                result = await whois_f(domain)
                if len(result) <= 1994:
                    await ctx.send(f"```{result}```")
                else:
                    now = datetime.now()
                    filename = f"./whois/{now}_{ctx.author.id}.txt"
                    async with aiofiles.open(filename, 'a') as f:
                        await f.write(result)
                    await ctx.send(file=discord.File(filename))
                    os.remove(filename)
            else:
                await ctx.send(f"The domain returned an invalid IP!\n{text}")

def setup(client):
    client.add_cog(networkingtools(client))
