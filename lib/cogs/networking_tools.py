import discord, os, requests, passgen, socket, json, time, re, asyncio, math, aiofiles, asyncdns, async_timeout
from socket import gaierror
from datetime import datetime
from discord import Embed, colour
from discord.ext import commands
from aiohttp import request
from pygicord import Paginator
from bs4 import BeautifulSoup

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


async def bannergrab_f(ip, port):
    try:
        async with async_timeout.timeout(2):
            r, w = await asyncio.open_connection(ip, port)
    except asyncio.TimeoutError:
        return "target timed out"
    except ConnectionRefusedError:
        return "port closed"
    try:
        async with async_timeout.timeout(2):
            banner = await r.read(1024)

        w.close()
        if banner.decode().strip() == "":
            return "Port did not return a banner"
        else:
            return banner.decode().strip()
    except asyncio.TimeoutError:
        return "Port open but took too long to return a banner"



class networkingtools(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.common_ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143,
                             443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]

    @commands.command(name="iplookup", description="Provides geoinformation on an IP", aliases=["geoip", "ip", "ipinfo"])
    async def iplookup(self, ctx, ip=""):
        text = "Usage: ./iplookup [IP]"
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
                    await ctx.send(f"```Could not find {ip}\n{text}```")
            elif response.status == 429:
                await ctx.send(f"```Daily iplookup limit reached```")
            else:
                await ctx.send(f"```There was an issue with the API, please try again later!\n{text}```")

        @iplookup.error
        async def iplookup_error(self, ctx, error):
            text = "Usage: ./iplookup [IP]"
            if isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(f"```{text}```")


    @commands.command(name="passgen", description="generates a number of passwords with a given length", aliases=["passwordgenerator", "password"])
    async def passwords(self, ctx, length: int, number=1):
        text = "Usage: ./passgen [length] (number)"
        if number <= 25 and number >= 1:
            if length <= 25 and length >= 4:
                embed = Embed(title="Passwords ",
                              description=f"{number} passwords of {length} length",
                              colour=discord.Colour.red())
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
            await ctx.send(f"```Please enter the number of passwords and the length\n{text}```")
        else:
            raise

    @commands.command(name="ping", description="Pings any provided IP")
    async def ping(self, ctx, ip: str, count: int = 3):
        text = "Usage: ./ping [ip] (count)\nMax count is 10"
        try:
            ip = socket.gethostbyname(ip)
        except socket.gaierror:
            await ctx.send(f"```{ip} was unresponsive\n{text}```")
        else:
            if validate_ip(ip) is True:
                if count <= 10:
                    output = await ping_f(ip, count)
                    await ctx.send(f"```{output}```")
                else:
                    await ctx.send(f"```You may only have up to 10 ping requests\n{text}```")
            else:
                await ctx.send(f"```Please enter a valid IP address\n{text}```")

    @ping.error
    async def ping_error(self, ctx, error):
        text = "Usage: ./ping [ip] (count)\nMax count is 10"
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"```{text}```")
        else:
            await ctx.send(f"```An unknown error has occured!\n{text}```")
            raise error

    @commands.command(name="cvesearch", description="Search CVEs on https://cve.circl.lu/", alises=["cveid", "cvelookup"])
    async def cvesearch(self, ctx, search_type, query=""):
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
        search_type = search_type.lower()
        if query == "":
            if search_type == "dbinfo":
                async with request("GET", f"https://cve.circl.lu/api/dbInfo", headers={}) as r:
                    if r.status == 200:
                        data = await r.json()
                        embed = Embed(title="Database information", description="https://cve.circl.lu/", colour=discord.Colour.red())
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
                        if not "availability" in impact.keys():
                            impact['availability'] = "N/A"
                        if not "confidentiality" in impact.keys():
                            impact["confidentiality"] = "N/A"
                        if not "integrity" in impact.keys():
                            impact["integrity"] = "N/A"
                        try:
                            access = last['access']
                        except KeyError:
                            pass
                        else:
                            if not "authentication" in access.keys():
                                access["authentication"] = "N/A"
                            if not "complexity" in access.keys():
                                access["complexity"] = "N/A"
                            if not "vector" in access.keys():
                                access["vector"] = "N/A"
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
                                embed = Embed(title=f"Browse results for {query}", colour=discord.Colour.red())
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
                        overview = Embed(title=f"CVE Overview: {query}", colour=discord.Colour.red())
                        overview.add_field(name="Last modified: ", value=data['Modified'], inline=False)
                        overview.add_field(name="Published: ", value=data['Published'], inline=False)
                        overview.add_field(name="Assigner: ", value=data['assigner'], inline=False)
                        access = data["access"]
                        try:
                            overview.add_field(name="Authentication: ", value=access['authentication'], inline=False)
                        except KeyError:
                            overview.add_field(name="Authentication: ", value="N/A", inline=False)
                        try:
                            overview.add_field(name="Complexity: ", value=access['complexity'], inline=False)
                        except KeyError:
                            overview.add_field(name="Complexity: ", value="N/A", inline=False)
                        try:
                            overview.add_field(name="Vector: ", value=access['vector'])
                        except KeyError:
                            overview.add_field(name="Vector: ", value="N/A")
                        overview.set_footer(text="CVE results from https://cve.circl.lu/")
                        pages.append(overview)

                        refs = data['references']
                        try:
                            refs = refs[0:10]
                        except IndexError:
                            pass
                        references = Embed(title="References", colour=discord.Colour.red())
                        for r in refs:
                            references.add_field(name="⠀", value=r, inline=False)
                        pages.append(references)
                        if "capec" in data.keys():
                            capecs = data['capec']
                            try:
                                capecs = capecs[0:3]
                            except IndexError:
                                pass
                            for c in capecs:
                                embed = Embed(title=c['name'], colour=discord.Colour.red())
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

    @cvesearch.error
    async def cvesearch_error(self, ctx, error):
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
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"```{text}```")
        else:
            await ctx.send(f"```An unknown error has occured!\n{text}```")
            raise error

    @commands.command(name="bannergrab", description="Grabs a banner from a port", aliases=["service"])
    async def bannergrab(self, ctx, ip, port):
        text = "Usage: ./bannergrab [IP] [Port]"
        try:
            ip = socket.gethostbyname(ip)
            if validate_ip(ip) is True:
                if validate_port(port) is True:
                    banner = await bannergrab_f(ip, port)
                    negatives = ["Port did not return a banner", "port closed", "target timed out"]
                    if banner in negatives:
                        response = f"""```diff
- {ip}:{port}:{banner} ```"""
                    else:
                        response = f"""```diff
+ {ip}:{port}:{banner} ```"""
                    await ctx.send(f"{response}")
                else:
                    await ctx.send(f"```Invalid port selected\n{text}```")
            else:
                await ctx.send(f"```Invalid IP\n{text}```")
        except socket.gaierror:
            await ctx.send(f"```Unable to connect to IP\n{text}```")

    @bannergrab.error
    async def bannergrab_error(self, ctx, error):
        text = "Usage: ./bannergrab [IP] [Port]"
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"```{text}```")
        else:
            await ctx.send(f"```An unknown error has occured!\n{text}```")
            raise error

    @commands.command(name="dnsquery", description="Perform DNS queries")
    async def dnsquery(self, ctx, domain, query):
        text = """
Usage: ./dnsquery [domain] [query]

Supported queries:
A, NS, CNAME, SOA, MX, TXT, RP, AAAA, LOC, SRV, IPSECKEY, SSHHFP, DNSKEY,
ANY
"""
        query = query.lower()
        if query == "a":
            parsed_query = 1
        elif query == "ns":
            parsed_query = 2
        elif query == "cname":
            parsed_query = 5
        elif query == "soa":
            parsed_query = 6
        elif query == "mx":
            parsed_query = 15
        elif query == "txt":
            parsed_query = 16
        elif query == "rp":
            parsed_query = 17
        elif query == "aaaa":
            parsed_query = 28
        elif query == "loc":
            parsed_query = 29
        elif query == "srv":
            parsed_query = 33
        elif query == "ipseckey":
            parsed_query = 45
        elif query == "sshhfp":
            parsed_query = 44
        elif query == "dnskey":
            query = 48
        elif query == "any":
            parsed_query = 255
        else:
            parsed_query = None
        if parsed_query is not None:
            resolver = asyncdns.SmartResolver()
            query = asyncdns.Query(domain, parsed_query, 1)
            response = await resolver.lookup(query)
            try:
                await ctx.send(f"```{response}```")
            except:
                filename = f"./dnsqueries/{ctx.author.id}.txt"
                async with aiofiles.open(filename, 'a') as f:
                    await f.write(response)
                await ctx.author.send(file=discord.File(filename))
                os.remove(filename)
        else:
            await ctx.send(f"```Unable to parse query, please choose a supported query\n{text}```")

    @dnsquery.error
    async def dnsquery_error(self, ctx, error):
        text = """
Usage: ./dnsquery [domain] [query]

Supported queries:
A, NS, CNAME, SOA, MX, TXT, RP, AAAA, LOC, SRV, IPSECKEY, SSHHFP, DNSKEY, ANY
"""
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"```{text}```")
        else:
            await ctx.send(f"```An unknown error has occured\n{text}```")
            raise error

    @commands.cooldown(2, 30, commands.BucketType.user)
    @commands.command(name="portscan", description="Scan for open ports", aliases=["servicescan"])
    async def portscan(self, ctx, ip, *, ports=None):
        text = """
Usage: ./portscan [ip] (ports)
Please seperate ports with ','

Note: Default ports are top 20 most common, max is 100"""
        try:
            ip = socket.gethostbyname(ip)
            check = validate_ip(ip)
        except socket.gaierror:
            check = False
        if check is True:
            if ports is None:
                ports = self.common_ports
                valid = True
            else:
                ports = ports.split(",")
                if len(ports) <= 100:
                    for port in ports:
                        valid = validate_port(port)
                        if valid is False:
                            await ctx.send(f"```Invalid port: {port}\n{text}```")
                            break

                else:
                    await ctx.send(f"```You may only scan up to 100 ports\n{text}```")
                    valid = False
            if valid is not False:
                results = []
                scanned_ports = []
                for port in ports:
                    if port not in scanned_ports:
                        scanned_ports.append(port)
                        results.append([port, await bannergrab_f(ip, int(port))])
                results_str = ""
                for x in results:
                    if x[1] == "port closed":
                        results_str += f"- {x[0]}: {x[1]}\n"
                    else:
                        results_str += f"+ {x[0]}: {x[1]}\n"
                if len(results_str) <= 1992:
                    await ctx.send(f"```diff\n{results_str}```")
                else:
                    filename = f"./scans/{ctx.author.id}.txt"
                    async with aiofiles.open(filename, 'a') as f:
                        await f.write(results_str)
                        await ctx.send(file=discord.File(filename))
                    os.remove(filename)

        else:
            await ctx.send(f"```Invalid IP or bot was unable to resolve IP from domain name\n{text}```")

    @portscan.error
    async def portscan_error(self, ctx, error):
        text = """
Usage: ./portscan [ip] (ports)
Please seperate ports with ','

Note: Default ports are top 20 most common, max is 100"""
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"```Command is on cooldown, please wait {round(error.retry_after, 2)} seconds\n{text}```")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"```{text}```")
        else:
            await ctx.send(f"```An unknown error has occured\n{text}```")
            raise error

def setup(client):
    client.add_cog(networkingtools(client))
