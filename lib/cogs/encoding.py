import discord, base64, re, os, hashlib
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from discord import Embed, Colour

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

    @commands.command(name="md5encrypt", description="Hashes a string using MD5", aliases=["md5"])
    async def md5encrypt(self, ctx, message: str):
        hashed = hashlib.md5(message.encode())
        await ctx.send(f"Your string hashed is: {hashed.hexdigest()}")

    @md5encrypt.error
    async def md5(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a string to hash")
        else:
            raise


def setup(client):
    client.add_cog(encoding(client))
