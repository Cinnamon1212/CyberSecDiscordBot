import discord, base64, re, os, hashlib, subprocess
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from discord import Embed, Colour
from Crypto.Cipher import AES

class encoding(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="base64encode", description="Base64 encodes a string", aliases=["B64e"])
    async def base64encode(self, ctx, string: str):
        if len(string) <= 1490:
            encoded = base64.b64encode(bytes(string, 'ascii'))
            await ctx.send(str(encoded))
        else:
            await ctx.send("You may only have up to 1490 characters")

    @base64encode.error
    async def base64encode_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please provide a string to encode")
        else:
            raise

    @commands.command(name="base64decode", description="Decodes base64 to a string", aliases=["B64d"])
    async def base64decode(self, ctx, base64message: str):
        base64_bytes = base64message.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        string = message_bytes.decode('ascii')
        await ctx.send(f"Your decoded base64 is {string}")

    @base64decode.error
    async def base64decode_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please provide a string to decode")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("Please enter a base64 string to decode")
        else:
            raise

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
                      colour = discord.Colour.random())
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
    async def deCaeser(self, ctx, message: str):
        if len(message) <= 10:
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
            await ctx.send("The string may only be up to 10 characters")

    @deCaeser.error
    async def decaeser_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Please wait {error.retry_after} before using this command")

    @commands.command(name="hash", description="Hashes a string using a given algorithm (MD5, SHA1, SHA224, SHA256, SHA384 and SHA512)", aliases=["hashstring", "crypt"])
    async def hash(self, ctx, hashtype, *, message: str):
        if hashtype == "md5" or hashtype == "MD5":
            hashed = hashlib.md5(message.encode())
            await ctx.send(f"Your string hashed in {hashtype} is: {hashed.hexdigest()}")
        elif hashtype == "sha1" or hashtype == "SHA1":
            hashed = hashlib.sha1(message.encode())
            await ctx.send(f"Your string hashed in {hashtype} is: {hashed.hexdigest()}")
        elif hashtype == "sha224" or hashtype == "SHA224":
            hashed = hashlib.sha224(message.encode())
            await ctx.send(f"Your string hashed in {hashtype} is: {hashed.hexdigest()}")
        elif hashtype == "sha256" or hashtype == "SHA256":
            hashed = hashlib.sha256(message.encode())
            await ctx.send(f"Your string hashed in {hashtype} is: {hashed.hexdigest()}")
        elif hashtype == "sha384" or hashtype == "SHA384":
            hashed = hashlib.sha384(message.encode())
            await ctx.send(f"Your string hashed in {hashtype} is: {hashed.hexdigest()}")
        elif hashtype == "sha512" or hashtype == "SHA512":
            hashed = hashlib.sha512(message.encode())
            await ctx.send(f"Your string hashed in {hashtype} is: {hashed.hexdigest()}")
        else:
            await ctx.send("Please choose an algorithm out of: MD5, SHA1, SHA224, SHA256, SHA384 and SHA512")



    @hash.error
    async def hash_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a string to hash")
        else:
            raise

    @commands.command(name="hash-identifier", description="Tries to identify a hash", aliases=["hashid", "hashidentifier"])
    async def hashidentifier(self, ctx, hash: str):
        symbols = "!$%^&*()_+|~-=`{}[]:\";'<>?,./"
        if any(c in symbols for c in hash):
            await ctx.send("Invalid hash")
        else:
            hashid = subprocess.run(["hashid", f"{hash}", "-j"], stdout=subprocess.PIPE, text=True)
            await ctx.send(f"```\n{hashid.stdout}```")

    @hashidentifier.error
    async def hashid_error(self, ctx, error):
        if isinstance(error.commands.MissingRequiredArgument):
            await ctx.send("Please enter a hash to identify")
        else:
            raise

def setup(client):
    client.add_cog(encoding(client))
