import discord, os, requests, json, exiftool, faker, aiofiles, asyncio, re
from async_timeout import timeout
from faker.providers import bank, credit_card, phone_number
from discord import Embed
from discord.ext import commands
from aiohttp import request

with open('secrets.json', 'r') as secrets:
    data = secrets.read()
keys = json.loads(data)
securitytrailskey = keys['securitytrails']

def chase_redirects(url):
    while True:
        yield url
        r = requests.head(url)
        if 300 < r.status_code < 400:
            url = r.headers['location']
        else:
            break


class websites(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="StatusCheck", aliases=["Websitestatus", "webstatus", "httpstatus"], description="Used for getting http response code of a web page")
    async def website(self, ctx, url=""):
        if url == "":
            await ctx.send("Usage: ./webstatus (url)")
        else:
            async with request("GET", url) as resp:
                await ctx.send(f"website returned: {resp.status}")

    @commands.command(name="emailchecker", description="Verifies if an email is real or not", aliases=["emailverify", "emailinfo"])
    async def emailchecker(self, ctx, email: str):
        with open('secrets.json', 'r') as secrets:
            data1 = secrets.read()
        hunterapikey = json.loads(data1)
        apikey = hunterapikey['hunteriokey']
        url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={apikey}"
        async with request("GET", url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                embed = Embed(title="Email check",
                              description=f"checking {email}",
                              colour=discord.Colour.red())
                embed.add_field(name="Status: ", value=data['data']['status'])
                embed.add_field(name="Result: ", value=data['data']['result'])
                embed.add_field(name="Score: ", value=data['data']['score'])
                if data['data']['regexp'] is False:
                    embed.add_field(name="Valid format?", value="Invalid email format")
                elif data['data']['regexp'] is True:
                    embed.add_field(name="Valid format?", value="Valid email format")
                else:
                    embed.add_field(name="Valid format?", value="Unable to check!")

                if data['data']['smtp_server'] is False:
                    embed.add_field(name="SMTP check: ", value="Invalid SMTP server")
                elif data['data']['smtp_server'] is True:
                    embed.add_field(name="SMTP check: ", value="Valid SMTP server")
                else:
                    embed.add_field(name="SMTP check: ", value="Unable to validate!")

                if data['data']['mx_records'] is False:
                    embed.add_field(name="MX Records?", value="No available records")
                elif data['data']['mx_records'] is True:
                    embed.add_field(name="MX Records?", value="Existing records")
                else:
                    embed.add_field(name="MX Records?", value="Unable to check!")

                if data['data']['gibberish'] is False:
                    embed.add_field(name="Gibberish email?", value="Looks like it makes sense")
                elif data['data']['gibberish'] is True:
                    embed.add_field(name="Gibberish email?", value="Complete nonsense m8")
                else:
                    embed.add_field(name="Gibberish email?", value="Unable to check!")

                time = ctx.message.created_at
                embed.set_footer(text=f"Asked by {ctx.author.name} " + time.strftime("%d/%m/%y %X"))
                await ctx.send(embed=embed)
            elif response.status == 400:
                await ctx.send("```That's not an email!\nUsage: ./emailchecker [email]```")
            else:
                await ctx.send("There was an issue with the API!")

    @emailchecker.error
    async def emailchecker_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("```Usage: ./emailchecker [email]```")
        else:
            raise

    @commands.command(name="IdentityGenerator", description="Generates fake personal information", aliases=["Faker", "FakeID"])
    async def IdentityGenerator(self, ctx):
        fake = faker.Faker()
        embed = Embed(title="Here is your fake identity, enjoy!",
                      description=f"Full name: {fake.name()}",
                      colour=discord.Colour.red())
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Anonymous_emblem.svg/160px-Anonymous_emblem.svg.png")
        embed.add_field(name="Email: ", value=fake.email(), inline=False)
        embed.add_field(name="URL: ", value=fake.url(), inline=False)
        embed.add_field(name="Address: ", value=fake.address(), inline=False)
        embed.add_field(name="Credit card: ", value=fake.credit_card_full(), inline=False)
        embed.add_field(name="SSN: ", value=fake.ssn(), inline=False)
        embed.add_field(name="Hostname: ", value=fake.hostname(), inline=False)
        embed.add_field(name="IP Address: ", value=fake.ipv4_public(), inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="RedirectChaser", description="Finds all redirects associated with a link", aliases=["Wheregoes", "RedirectChecker"])
    async def redirectchaser(self, ctx, url=None):
        text = "Usage: ./wheregoes [URL]"
        if url is None:
            await ctx.send(f"```{text}```")
        else:
            try:
                requests.get(url)
            except requests.ConnectionError:
                await ctx.send(f"Unable to connect to {url}\n{text}")
            urls = []
            for url_redirects in chase_redirects(url):
                urls.append(url_redirects)
            embed = Embed(title=f"Redirects for {url}",
                          colour=discord.Colour.red())
            num = 1
            for url in urls:
                embed.add_field(name=f"Redirect #{num}", value=url, inline=False)
                num += 1
            await ctx.send(embed=embed)

    @commands.command(name="subdomain", description="Find subdomains", aliases=["sdomains"])
    async def findsubdomains(self, ctx, domain=None):
        text = "Usage: ./subdomain [domain]"
        if domain is None:
            await ctx.send(f"```{text}```")
        else:
            url = f"https://api.securitytrails.com/v1/domain/{domain}/subdomains"
            querystring = {"children_only": "false", "include_inactive": "true"}
            headers = {"Accept": "application/json", "apikey": securitytrailskey}
            async with request("GET", url, headers=headers, params=querystring) as response:
                if response.status == 200:
                    data = await response.json()
                    Found_Subdomains = data['subdomains']
                    if len(Found_Subdomains) == 0:
                        await ctx.send(f"```No subdomain records found!\n{text}```")
                    else:
                        subdomains = "First 10 subdomains:"
                        for sub in Found_Subdomains[:20]:
                            subdomains += f"\n{sub}.{domain}"
                        await ctx.send(f"```{subdomains}```")
                else:
                    await ctx.send(f"```There was an issue with the API\n{text}```")




def setup(client):
    client.add_cog(websites(client))
