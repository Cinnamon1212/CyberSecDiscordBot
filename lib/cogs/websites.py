import discord, os, requests, json, exiftool, faker, aiofiles
from faker.providers import bank, credit_card, phone_number
from discord import Embed, colour
from discord.ext import commands
from aiohttp import request
from pyppeteer import launch
from pyppeteer.errors import PageError

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

async def webss_f(ctx, url, w, h):
    await ctx.send("Attempting to grab the web page, some pages may block tor connections")
    UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36"
    try:
        browser = await launch(headless=True)
        page = await browser.newPage()
        await page.setViewport({"width": w, "height": h})
        await page.setUserAgent(UA)
        await page.goto(url)
        await page.screenshot({'path': f"./webpages/{ctx.author.id}.png"})
        await browser.close()
        return True
    except PageError:
        return None


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
        if not ctx.message.attachments:
            await ctx.send("```Usage: ./exiftool // Attach a file to the message```")
        else:
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
                async with aiofiles.open(f"./exiftool/{ctx.author.id}_{attachment_name}.txt", mode="x") as f:
                    await f.write(metadata)
                await ctx.send(file=discord.File(f"./exiftool/{ctx.author.id}_{attachment_name}.txt"))
                os.remove(f"./exiftool/{ctx.author.id}_{attachment_name}")  # Removes provided file
                os.remove(f"./exiftool/{ctx.author.id}_{attachment_name}.txt")

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
                          colour=discord.Colour.random())
            num = 1
            for url in urls:
                embed.add_field(name=f"Redirect #{num}", value=url, inline=False)
                num += 1
            await ctx.send(embed=embed)

    @commands.command(name="WebScreenshot", description="Takes a screenshot of a URL", aliases=["WebSS", "GrabPage"])
    async def WebScreenshot(self, ctx, url=None, width=1920, height=1080):
        text = """Usage: ./webss [URL] (width) (height)

Default width = 1920
Default height = 1080

If the page fails to render, try pass the full URL (example: https://www.google.com/)"""
        if url is None:
            await ctx.send(f"```{text}```")
        else:
            try:
                width = int(width)
                height = int(height)
            except ValueError:
                await ctx.send(f"```Please pass width and height as numbers.\n{text}```")
            else:
                returnvalue = await webss_f(ctx, url, width, height)
                if returnvalue is None:
                    await ctx.send(f"```Unable to render {url}!\n{text}```")
                else:
                    await ctx.send(f"Here is a screenshot of: {url}", file=discord.File(f"./webpages/{ctx.author.id}.png"))
                    os.remove(f"./webpages/{ctx.author.id}.png")

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
