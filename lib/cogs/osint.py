import discord, json, magic, os, aiofiles, re, imageio
from bs4 import BeautifulSoup
from PIL import Image, ExifTags
from discord import Embed
from discord.ext import commands
from aiohttp import request
from pygicord import Paginator
from datetime import datetime

with open('secrets.json', 'r') as secrets:
    data = secrets.read()
keys = json.loads(data)
apikey = keys['googleapi']
builtwithkey = keys['builtwith']


async def get_imagemeta(file):
    pic = imageio.imread(file)
    type = Image.open(file)
    megapixels = (type.size[0]*type.size[1]/1000000)
    d = re.sub(r'[a-z]', '', str(pic.dtype))
    t = len(Image.Image.getbands(type))

    results = f"""

Format: {type.format}
Data type: {pic.dtype}
Bit depth (per channel): {d}
Bit depth (per pixel): {int(d)*int(t)}
Mode: {type.mode}
Palette: {type.palette}
Width: {type.size[0]}
Height: {type.size[1]}
Megapixels: {megapixels}

"""
    return results

async def parse_dork(dork):
    if dork == 1:
        parsed = 'intitle:"index of" "credentials.xml" | "credentials.inc" | "credentials.txt"'
    elif dork == 2:
        parsed = 'intitle:"Index of /" +.htaccess'
    elif dork == 3:
        parsed = "filetype:log"
    elif dork == 4:
        parsed = "inurl:/proc/self/cwd"
    elif dork == 5:
        parsed = 'intitle:"index of" inurl:ftp'
    elif dork == 6:
        parsed = "intitle:index.of id_rsa -id_rsa.pub"
    elif dork == 7:
        parsed = 'filetype:xls inurl:"email.xls"'
    elif dork == 8:
        parsed = 'inurl:zoom.us/j and intext:scheduled for'
    elif dork == 9:
        parsed = 'inurl:"/phpmyadmin/user_password.php"'
    elif dork == 10:
        parsed = 'intitle:"Apache2 Ubuntu Default Page: It works"'
    elif dork == 11:
        parsed = 'intitle:"IIS Windows Server" -inurl:"IIS Windows Server"'
    elif dork == 12:
        parsed = 'intitle:index.of.?.sql'
    elif dork == 13:
        parsed = '"Index of" inurl:htdocs inurl:xampp'
    elif dork == 14:
        parsed = 'intitle:"Please Login" inurl:"/remote/login?lang=en"'
    elif dork == 15:
        parsed = '"USB Port 1 (Public Data)" + "USB Port 2 (Public Data)" "Status" -pdf'
    elif dork == 16:
        parsed = 'inurl:"index.php?id=" intext:"Warning: mysql_num_rows()"'
    elif dork == 17:
        parsed = '"cpanel username" "cpanel password" ext:txt'
    elif dork == 18:
        parsed = 'intitle:"index of" "idx_config"'
    elif dork == 19:
        parsed = '"\'username\' =>" + "\'password\' =>" ext:log'
    elif dork == 19:
        parsed = 'intitle:"index of" "/master.passwd"'
    else:
        parsed = None
    if parsed is None:
        return None
    else:
        return parsed


class osint(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.url_regex = re.compile(
                r'^(?:http|ftp)s?://'
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
                r'localhost|'
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
                r'(?::\d+)?'
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    @commands.command(name="instagramlookup", description="Search for Instagram users", aliases=["instausers"])
    async def instagramlookup(self, ctx, *, username=None):
        text = "./instagramlookup [username]"
        if username is None:
            await ctx.send(f"```{text}```")
        else:
            if username[0] == "@":
                username = username[1:]
            async with request("GET", f"https://www.instagram.com/{username}/") as resp:
                if resp.status == 404:
                    first = None
                else:
                    first = username
            url = f"https://searchusers.com/search/{username}"
            async with request("GET", url) as response:
                if response.status == 200:
                    html = await response.text()
                else:
                    await ctx.send(f"```Website returned code: {response.status}, please try again later\n{text}```")
                    html = None

            if html is not None:
                soup = BeautifulSoup(html, 'html.parser')
                accounts = soup.find_all(class_="timg")
                account_links = ""
                if first is not None:
                    account_links += f"\n+ {first}"

                for account in accounts:
                    x = account.get("href")
                    if x is not None:
                        account_links += f"\n+ {x[29:]}"
                await ctx.send(f"""
```diff
{account_links}```""")

    @commands.command(name="facebooklookup", description="Search for Facebook users", aliases=["fbusers"])
    async def facebooklookup(self, ctx, *, username=None):
        text = "Usage: ./facebooklookup [username]"
        if username is None:
            await ctx.send(f"```{text}```")
        else:
            q = username
            cx = "09982abed469e58ff"
            url = f"https://www.googleapis.com/customsearch/v1?key={apikey}&cx={cx}&q={q}&start=1"
            async with request("GET", url) as response:
                search_response = await response.json()
            try:
                account_links = ""
                x = 1
                for item in search_response['items']:
                    if item['formattedUrl'] not in account_links:
                        account_links += f"\n+ {item['formattedUrl']}"
                    if x == 30:
                        break
                    x += 1

                await ctx.send(f"""
```diff
{account_links}```""")
            except KeyError:
                await ctx.send(f"```No search results found for {username}\n{text}```")

    @commands.command(name="twitterlookup", description="Search for Twitter users", aliases=["twitterusers"])
    async def twitterlookup(self, ctx, *, username=None):
        text = "Usage: ./twitterlookup [username]"
        if username is None:
            await ctx.send(f"```{text}```")
        else:
            q = username
            cx = "fd1dde45779087b24"
            url = f"https://www.googleapis.com/customsearch/v1?key={apikey}&cx={cx}&q={q}&start=1"
            async with request("GET", url) as response:
                search_response = await response.json()
            try:
                account_links = ""
                x = 1
                for item in search_response['items']:
                    if item['formattedUrl'] not in account_links:
                        account_links += f"\n+ {item['formattedUrl']}"
                    if x == 30:
                        break
                    x += 1

                await ctx.send(f"""
```diff
{account_links}```""")
            except KeyError:
                await ctx.send(f"```No search results found for {username}\n{text}```")


    @commands.command(name="getdomain", description="Find detailed information for a domain", aliases=["domaininfo"])
    async def getdomain(self, ctx, domain=None):
        text = "Usage: ./getdomain [domain]\n\nNote that only the root domain will be checked."
        if domain is None:
            await ctx.send(f"```{text}```")
        else:
            url = f"https://api.builtwith.com/free1/api.json?KEY={builtwithkey}&LOOKUP={domain}"
            async with request("GET", url) as response:
                if response.status == 200:
                    data = await response.json()
                else:
                    await ctx.send(f"```Website returned code: {response.status}, please try again later\n{text}```")
                    data = None
            if data is not None:
                embeds = []
                embed = Embed(title=data['domain'], colour=discord.Colour.red())
                embed.add_field(name="First time domain was indexed: ", value=datetime.fromtimestamp(data['first']), inline=False)
                embed.add_field(name="Last time domain was indexed: ", value=datetime.fromtimestamp(data['last']), inline=False)
                embed.add_field(name="Number of groups: ", value=len(data['groups']), inline=False)
                embeds.append(embed)
                x = 1
                for group in data['groups']:
                    embed = Embed(title=f"Group #{x}: {group['name']}", colour=discord.Colour.red())
                    embed.add_field(name="Group name", value=group['name'], inline=False)
                    if len(group['categories']) >= 22:
                        categories = group['categories'][22:]
                    else:
                        categories = group['categories']
                    y = 1
                    for category in categories:
                        embed.add_field(name=f"Category #{y}: ", value=category['name'], inline=False)
                        embed.add_field(name="Live technologies: ", value=category['live'], inline=False)
                        embed.add_field(name="Dead technologies: ", value=category['dead'], inline=False)
                        y += 1
                    embeds.append(embed)
                    x += 1
                paginator = Paginator(pages=embeds)
                await paginator.start(ctx)

    @commands.command(name="imagedata", description="Retrieve image data", aliases=["imagemeta"])
    async def imagedata(self, ctx, url=None):
        text = """
Usage: ./imagedata [url/attach file to message]
If you pass a URL, ensure the URL links directly to the image"""
        images_extensions = ['.jpg', '.jpeg', '.jpe', '.jif', ' .jfif',
                             '.jfi', '.png', '.gif', '.webp', '.tiff', '.tif'
                             '.psd', '.raw', '.arw', '.cr2', '.nrw', '.k25',
                             '.bmp', '.dib', '.heif', '.heic', '.ind', '.indd',
                             '.indt', '.jp2', '.j2k', '.jpf', '.jpx', '.jpm',
                             '.mj2', '.svg', '.svgz']
        if ctx.message.attachments:
            attachment_name = ctx.message.attachments[0].filename
            extension = f".{attachment_name.split('.')[-1]}"
            if '/' in attachment_name:
                await ctx.send(f"```File names may not contain /\'s\n{text}```")
            elif extension not in images_extensions:
                await ctx.send(f"```Unaccepted file extension\n{text}```")
            else:
                attachment_url = ctx.message.attachments[0].url
                async with request("GET", attachment_url) as r:
                    file_content = await r.read()
                file_path = f"./exiftool/{ctx.author.id}_{attachment_name}"
                async with aiofiles.open(file_path, 'ab') as f:
                    await f.write(file_content)
                if "image/" in magic.from_file(file_path, mime=True).lower():
                    check = True
                else:
                    await ctx.send(f"```Unsupported mime type\n{text}```")
                    os.remove(file_path)
                    check = False
        else:
            if url is not None:
                if re.match(self.url_regex, url) is not None:
                    extension = f".{url.split('.')[-1]}"
                    if extension not in images_extensions:
                        await ctx.send(f"```Unaccepted file extension\n{text}```")
                    else:
                        async with request("GET", url) as resp:
                            if resp.status == 200:
                                if "image/" not in resp.content_type.lower():
                                    await ctx.send(f"```URL is not an image file\n{text}```")
                                    file_content = None
                                else:
                                    try:
                                        if int(resp.headers['Content-Length']) < 8000000:
                                            file_content = await resp.read()
                                    except KeyError:
                                        file_content = None
                                        await ctx.send(f"```Unable to verify file size\n{text}```")
                            else:
                                await ctx.send(f"```URL returned {resp.status}\n{text}```")
                                file_content = None
                        if file_content is not None:
                            file_path = f"./exiftool/{ctx.author.id}.{resp.content_type.lower().split('/')[1]}"
                            async with aiofiles.open(file_path, 'ab') as f:
                                await f.write(file_content)
            else:
                file_path = None
                await ctx.send(f"```{text}```")

        if file_path is not None:
            metadata = await get_imagemeta(file_path)
            await ctx.send(f"```{metadata}```")

    @commands.command(name="googledork", description="Search for google dorks", aliases=["dork", "dorksearch"])
    async def googledork(self, ctx, dork=None):
        text = """
Usage: ./googledork [dork]

Predfined dorks:
(1) Find credidential file
(2) .htaccess
(3) *.log files
(4) /proc/self/cwd
(5) FTP
(6) SSH keys
(7) Email.xls
(8) Zoom videos
(9) PHP My admin panel
(10) Apache2 Ubuntu
(11) IIS Windows server
(12) .sql files
(13) XAMPP Servers
(14) Remote IOT device login
(15) IOT devices with USB info
(16) MySQL num rows error
(17) Cpanel login creds
(18) idx config
(19) master.passwd files

You may pass your own dork, but you must escape any quotation marks with \\
"""

        if dork is None:
            await ctx.send(f"```{text}```")
        else:
            try:
                dork = int(dork)
                dork = await parse_dork(dork)

            except:
                pass
            q = dork
            cx = "f3399d8071477b58e"
            url = f"https://www.googleapis.com/customsearch/v1?key={apikey}&cx={cx}&q={q}&start=2"
            async with request("GET", url) as response:
                search_response = await response.json()
            try:
                dork_links = ""
                if len(search_response['items']) <= 30:
                    for item in search_response['items']:
                        if "..." in item['formattedUrl']:
                            dork_links += f"\n+ {item['link']}"
                        else:
                            dork_links += f"\n+ {item['formattedUrl']}"
                else:
                    x = 1
                    for item in search_response['items'][10:]:
                        dork_links += f"\n+ {item['link']}"
                        if x == 30:
                            break
                        x += 1

                await ctx.send(f"""
```diff
{dork_links}```""")
            except KeyError:
                await ctx.send(f"```No search results found for {dork}\n{text}```")

    @googledork.error
    async def dork_error(self, ctx, error):
        text = """
Usage: ./googledork [dork]

Predfined dorks:
(1) Find credidential file
(2) .htaccess
(3) *.log files
(4) /proc/self/cwd
(5) FTP
(6) SSH keys
(7) Email.xls
(8) Zoom videos
(9) PHP My admin panel
(10) Apache2 Ubuntu
(11) IIS Windows server
(12) .sql files
(13) XAMPP Servers
(14) Remote IOT device login
(15) IOT devices with USB info
(16) MySQL num rows error
(17) Cpanel login creds
(18) idx config
(19) master.passwd files

You may pass your own dork, but you must escape any quotation marks with \\
        """
        if isinstance(error, commands.errors.UnexpectedQuoteError):
            await ctx.send(f"```Please escape \" with \\\n{text}```")

def setup(client):
    client.add_cog(osint(client))
