import discord, base64, re, os, hashlib, subprocess
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from discord import Embed, Colour

class encoding(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command("Caesercipher", description="Caeser Ciphers a given string", aliases=["caeser", "ROT"])
    async def caeser(self, ctx, shift: int, *, message: str):
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        alphabet = list(alphabet)
        message = list(message)
        cipher = ''

        for letter in message:
            if letter in alphabet:
                oldindex = alphabet.index(letter)
                newindex = (oldindex + shift) % len(alphabet)
                newletter = alphabet[newindex]
            else:
                newletter = letter
            cipher += newletter
        message = ''.join(c for c in message)
        embed = Embed(title="Caeser cipher",
                      description=f"Shift: {shift}",
                      colour=discord.Colour.random())
        embed.add_field(name="Original message: ", value = message)
        embed.add_field(name="Ciphered message: ", value = cipher)
        await ctx.send(embed=embed)

    @caeser.error
    async def caeser_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Please use ./caeser (shift) (message)")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please use ./caeser (shift) (message)")
        else:
            raise


    @commands.command("decaesercipher", description="bruteforces a ceaser cipher", aliases=["decodecaesercipher", "caeserdecode", "deCaeser"])
    @commands.cooldown(rate=1, per=10)
    async def deCaeser(self, ctx, *,message: str):
        if len(message) <= 25:
            hasNums = bool(re.search(r'\d', message))
            if hasNums is False:
                result = ""
                letters = "abcdefghijklmnopqrstuvwxyz"
                enc_string = message
                x = 0
                while x < 26:
                    x = x + 1
                    stringtodecrypt = enc_string
                    stringtodecrypt = stringtodecrypt.lower()
                    ciphershift = int(x)
                    stringdecrypted = ""
                    for character in stringtodecrypt:
                        position = letters.find(character)
                        newposition = position-ciphershift
                        if character in letters:
                            stringdecrypted = stringdecrypted + letters[newposition]
                        else:
                            stringdecrypted = stringdecrypted + character
                    ciphershift = ciphershift
                    result += f"\nShift: {ciphershift}\nResult:{stringdecrypted}\n"
                results = f"""```{result}```"""
                await ctx.author.send(results)

            else:
                result = ""
                letters = "abcdefghijklmnopqrstuvwxyz1234567890"
                enc_string = message
                x = 0
                while x < 36:
                    x = x + 1
                    stringtodecrypt = enc_string
                    stringtodecrypt = stringtodecrypt.lower()
                    ciphershift = int(x)
                    stringdecrypted = ""
                    for character in stringtodecrypt:
                        position = letters.find(character)
                        newposition = position-ciphershift
                        if character in letters:
                            stringdecrypted = stringdecrypted + letters[newposition]
                        else:
                            stringdecrypted = stringdecrypted + character
                    ciphershift = ciphershift
                    result += f"\nShift: {ciphershift}\nResult:{stringdecrypted}\n"
                results = f"""```{result}```"""
                await ctx.author.send(results)
        else:
            await ctx.send("The string may only be up to 25 characters")

    @deCaeser.error
    async def decaeser_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Please wait {error.retry_after} before using this command")

    @commands.command(name="hash", description="Hashes a string using a given algorithm (MD5, SHA1, SHA224, SHA256, SHA384 and SHA512)", aliases=["hashstring", "crypt"])
    async def hash(self, ctx, hashtype=None, *, message: str = None):
        text = """
Usage: ./hash [hashtype] [message]

Hash types:
[+] md5
[+] SHA1
[+] SHA224
[+] SHA256
[+] SHA384
[+] SHA512
[+] Blake2s
[+] Blake2b
"""
        if hashtype is None or message is None:
            await ctx.send(f"```{text}```")
        else:
            hashtype = hashtype.lower()
            if hashtype == "md5":
                hashed = hashlib.md5(message.encode())
                await ctx.send(f"Your string hashed in {hashtype} is: {hashed.hexdigest()}")
            elif hashtype == "md4":
                hashed = hashlib.new('md4', message.encode())
                await ctx.send(f"Your string hashed in {hashtype} is: {hashed.hexdigest()}")
            elif hashtype == "sha1":
                hashed = hashlib.sha1(message.encode())
                await ctx.send(f"Your string hashed in {hashtype} is: {hashed.hexdigest()}")
            elif hashtype == "sha224":
                hashed = hashlib.sha224(message.encode())
                await ctx.send(f"Your string hashed in {hashtype} is: {hashed.hexdigest()}")
            elif hashtype == "sha256":
                hashed = hashlib.sha256(message.encode())
                await ctx.send(f"Your string hashed in {hashtype} is: {hashed.hexdigest()}")
            elif hashtype == "sha384":
                hashed = hashlib.sha384(message.encode())
                await ctx.send(f"Your string hashed in {hashtype} is: {hashed.hexdigest()}")
            elif hashtype == "sha512":
                hashed = hashlib.sha512(message.encode())
                await ctx.send(f"Your string hashed in {hashtype} is: {hashed.hexdigest()}")
            elif hashtype == "blake2b":
                hashed = hashlib.blake2b(message.encode())
                await ctx.send(f"Your string hashed in {hashtype} is: {hashed.hexdigest()}")
            elif hashtype == "blake2s":
                hashed = hashlib.blake2s(message.encode())
                await ctx.send(f"Your string hashed in {hashtype} is: {hashed.hexdigest()}")
            else:
                await ctx.send("Please choose an algorithm out of: MD5, SHA1, SHA224, SHA256, SHA384 and SHA512")


    @commands.command(name="hash-identifier", description="Tries to identify a hash", aliases=["hashid", "hashidentifier"])
    async def hashidentifier(self, ctx, hash_: str = None):
        text = "Usage: ./hashid [hash]"
        if hash_ is None:
            await ctx.send(f"```{text}```")
        else:
            symbols = "!$%^&*()_+|~-=`{}[]:\";'<>?,./"
            if any(c in symbols for c in hash_):
                await ctx.send(f"```Invalid hash\n{text}```")
            else:
                hashid = subprocess.run(["hashid", f"{hash_}", "-j"], stdout=subprocess.PIPE, text=True)
                if hashid.stdout.strip() != "":
                    await ctx.send(f"```{hashid.stdout}```")
                else:
                    await ctx.send(f"```Unable to identify hash\n{text}```")


def setup(client):
    client.add_cog(encoding(client))
