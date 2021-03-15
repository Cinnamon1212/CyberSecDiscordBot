import discord, os, requests, json, urllib3, exiftool, subprocess, faker, imgkit
from faker.providers import bank, credit_card, phone_number
from bs4 import BeautifulSoup
from discord import Embed, colour
from discord.ext import commands
from aiohttp import request


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
            await ctx.send("Please enter a url to check")
        else:
            http = urllib3.PoolManager()
            resp = http.request('GET', url)
            await ctx.send(f"website returned: {resp.status}")

    @website.error
    async def website_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter an email to check!")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please ensure you enter an email!")
        else:
            raise
            await ctx.send("An error has occured!")

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
                              colour=discord.Colour.random())
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
                await ctx.send("That's not an email!")
            else:
                await ctx.send("There was an issue with the API!")
                print(f"API returned {response.status}")

    @emailchecker.error
    async def emailchecker_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter an email to check!")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please ensure you enter an email!")
        else:
            raise
            await ctx.send("An error has occured!")

    @commands.command(name="IdentityGenerator", description="Generates fake personal information", aliases=["Faker", "FakeID"])
    async def IdentityGenerator(self, ctx):
        fake = faker.Faker()
        embed = Embed(title="Here is your fake identity, enjoy!",
                      description=f"Full name: {fake.name()}",
                      colour=discord.Colour.random())
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Anonymous_emblem.svg/160px-Anonymous_emblem.svg.png")
        embed.add_field(name="Email: ", value=fake.email(), inline=False)
        embed.add_field(name="URL: ", value=fake.url(), inline=False)
        embed.add_field(name="Address: ", value=fake.address(), inline=False)
        embed.add_field(name="Credit card: ", value=fake.credit_card_full(), inline=False)
        embed.add_field(name="SSN: ", value=fake.ssn(), inline=False)
        embed.add_field(name="Hostname: ", value=fake.hostname(), inline=False)
        embed.add_field(name="IP Address: ", value=fake.ipv4_public(), inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="exiftool", description="File information", aliases=["filedata", "fileinfo"])
    async def exiftool(self, ctx):
        attachment_name = ctx.message.attachments[0].filename
        attachment_url = ctx.message.attachments[0].url
        r = requests.get(attachment_url)
        with open(f"./exiftool/{ctx.author.id}_{attachment_name}", "wb") as f:
            f.write(r.content)
        f.close()
        with exiftool.ExifTool() as et:
            metadata = et.get_metadata(f"./exiftool/{ctx.author.id}_{attachment_name}")
        metadata = json.dumps(metadata, indent=4, sort_keys=True)
        if len(str(metadata)) < 2000:
            await ctx.send(f"""```json
{metadata}```""")
            os.remove(f"./exiftool/{ctx.author.id}_{attachment_name}")
        else:
            with open(f"./exiftool/{ctx.author.id}_{attachment_name}.txt", "x") as f:
                f.write(metadata)
                await ctx.send(file=discord.File(f"./exiftool/{ctx.author.id}_{attachment_name}.txt"))
                os.remove(f"./exiftool/{ctx.author.id}_{attachment_name}")
                os.remove(f"./exiftool/{ctx.author.id}_{attachment_name}.txt")

    @commands.command(name="RedirectChaser", description="Finds all redirects associated with a link", aliases=["Wheregoes", "RedirectChecker"])
    async def redirectchaser(self, ctx, url: str):
        try:
            response = requests.get(url)
        except requests.ConnectionError as exception:
            await ctx.send("Invalid URL")
        urls = []
        for url_redirects in chase_redirects(url):
            urls.append(url_redirects)
        embed = Embed(title=f"Redirects for {url}",
                      colour=discord.Colour.random())
        num = 1
        for url in urls:
            embed.add_field(name=f"Redirect #{num}", value=url, inline=False)
            num += 1
        await ctx.send(embed=embed)

    @commands.command(name="WebScreenshot", description="Takes a screenshot of a URL", aliases=["WebSS", "GrabPage"])
    async def WebScreenshot(self, ctx, url: str):
        options = {"width": "2000",
                   "disable-smart-width": ""}
        imgkit.from_url(url, f'./webpages/{ctx.author.id}.jpg', options=options)
        await ctx.send(f"Here is a screenshot of: {url}", file=discord.File(f"./webpages/{ctx.author.id}.jpg"))
        os.remove(f"./webpages/{ctx.author.id}.jpg")

    @WebScreenshot.error
    async def webss_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please provide a url")
        else:
            raise
def setup(client):
    client.add_cog(websites(client))
