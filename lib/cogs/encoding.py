import discord, base64, re, os, hashlib
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from discord import Embed, Colour

class encoding(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.HASHES = (
            ("Blowfish(Eggdrop)", "^\+[a-zA-Z0-9\/\.]{12}$"),
            ("Blowfish(OpenBSD)", "^\$2a\$[0-9]{0,2}?\$[a-zA-Z0-9\/\.]{53}$"),
            ("Blowfish crypt", "^\$2[axy]{0,1}\$[a-zA-Z0-9./]{8}\$[a-zA-Z0-9./]{1,}$"),
            (("DES(Unix)", "DES crypt", "DES hash(Traditional)"), "^.{0,2}[a-zA-Z0-9\/\.]{11}$"),
            ("MD5(Unix)", "^\$1\$.{0,8}\$[a-zA-Z0-9\/\.]{22}$"),
            (("MD5(APR)", "Apache MD5"), "^\$apr1\$.{0,8}\$[a-zA-Z0-9\/\.]{22}$"),
            ("MD5(MyBB)", "^[a-fA-F0-9]{32}:[a-z0-9]{8}$"),
            ("MD5(ZipMonster)", "^[a-fA-F0-9]{32}$"),
            (("MD5 crypt", "FreeBSD MD5", "Cisco-IOS MD5"), "^\$1\$[a-zA-Z0-9./]{8}\$[a-zA-Z0-9./]{1,}$"),
            ("MD5 apache crypt", "^\$apr1\$[a-zA-Z0-9./]{8}\$[a-zA-Z0-9./]{1,}$"),
            ("MD5(Joomla)", "^[a-fA-F0-9]{32}:[a-zA-Z0-9]{16,32}$"),
            ("MD5(Wordpress)", "^\$P\$[a-zA-Z0-9\/\.]{31}$"),
            ("MD5(phpBB3)", "^\$H\$[a-zA-Z0-9\/\.]{31}$"),
            ("MD5(Cisco PIX)", "^[a-zA-Z0-9\/\.]{16}$"),
            (("MD5(osCommerce)", "xt:Commerce"), "^[a-fA-F0-9]{32}:[a-zA-Z0-9]{2}$"),
            ("MD5(Palshop)", "^[a-fA-F0-9]{51}$"),
            ("MD5(IP.Board)", "^[a-fA-F0-9]{32}:.{5}$"),
            ("MD5(Chap)", "^[a-fA-F0-9]{32}:[0-9]{32}:[a-fA-F0-9]{2}$"),
            ("Juniper Netscreen/SSG (ScreenOS)", "^[a-zA-Z0-9]{30}:[a-zA-Z0-9]{4,}$"),
            ("Fortigate (FortiOS)", "^[a-fA-F0-9]{47}$"),
            ("Minecraft(Authme)", "^\$sha\$[a-zA-Z0-9]{0,16}\$[a-fA-F0-9]{64}$"),
            ("Lotus Domino", "^\(?[a-zA-Z0-9\+\/]{20}\)?$"),
            ("Lineage II C4", "^0x[a-fA-F0-9]{32}$"),
            ("CRC-96(ZIP)", "^[a-fA-F0-9]{24}$"),
            ("NT crypt", "^\$3\$[a-zA-Z0-9./]{8}\$[a-zA-Z0-9./]{1,}$"),
            ("Skein-1024", "^[a-fA-F0-9]{256}$"),
            (("RIPEMD-320", "RIPEMD-320(HMAC)"), "^[A-Fa-f0-9]{80}$"),
            ("EPi hash", "^0x[A-F0-9]{60}$"),
            ("EPiServer 6.x < v4", "^\$episerver\$\*0\*[a-zA-Z0-9]{22}==\*[a-zA-Z0-9\+]{27}$"),
            ("EPiServer 6.x >= v4", "^\$episerver\$\*1\*[a-zA-Z0-9]{22}==\*[a-zA-Z0-9]{43}$"),
            ("Cisco IOS SHA256", "^[a-zA-Z0-9]{43}$"),
            ("SHA-1(Django)", "^sha1\$.{0,32}\$[a-fA-F0-9]{40}$"),
            ("SHA-1 crypt", "^\$4\$[a-zA-Z0-9./]{8}\$[a-zA-Z0-9./]{1,}$"),
            ("SHA-1(Hex)", "^[a-fA-F0-9]{40}$"),
            (("SHA-1(LDAP) Base64", "Netscape LDAP SHA", "NSLDAP"), "^\{SHA\}[a-zA-Z0-9+/]{27}=$"),
            ("SHA-1(LDAP) Base64 + salt", "^\{SSHA\}[a-zA-Z0-9+/]{28,}[=]{0,3}$"),
            ("SHA-512(Drupal)", "^\$S\$[a-zA-Z0-9\/\.]{52}$"),
            ("SHA-512 crypt", "^\$6\$[a-zA-Z0-9./]{8}\$[a-zA-Z0-9./]{1,}$"),
            ("SHA-256(Django)", "^sha256\$.{0,32}\$[a-fA-F0-9]{64}$"),
            ("SHA-256 crypt", "^\$5\$[a-zA-Z0-9./]{8}\$[a-zA-Z0-9./]{1,}$"),
            ("SHA-384(Django)", "^sha384\$.{0,32}\$[a-fA-F0-9]{96}$"),
            ("SHA-256(Unix)", "^\$5\$.{0,22}\$[a-zA-Z0-9\/\.]{43,69}$"),
            ("SHA-512(Unix)", "^\$6\$.{0,22}\$[a-zA-Z0-9\/\.]{86}$"),
            (("SHA-384", "SHA3-384", "Skein-512(384)", "Skein-1024(384)"), "^[a-fA-F0-9]{96}$"),
            (("SHA-512", "SHA-512(HMAC)", "SHA3-512", "Whirlpool", "SALSA-10", "SALSA-20", "Keccak-512", "Skein-512",
              "Skein-1024(512)"), "^[a-fA-F0-9]{128}$"),
            ("SSHA-1", "^({SSHA})?[a-zA-Z0-9\+\/]{32,38}?(==)?$"),
            (("SSHA-1(Base64)", "Netscape LDAP SSHA", "NSLDAPS"), "^\{SSHA\}[a-zA-Z0-9]{32,38}?(==)?$"),
            (("SSHA-512(Base64)", "LDAP {SSHA512}"), "^\{SSHA512\}[a-zA-Z0-9+]{96}$"),
            ("Oracle 11g", "^S:[A-Z0-9]{60}$"),
            ("SMF >= v1.1", "^[a-fA-F0-9]{40}:[0-9]{8}&"),
            ("MySQL 5.x", "^\*[a-f0-9]{40}$"),
            (("MySQL 3.x", "DES(Oracle)", "LM", "VNC", "FNV-164"), "^[a-fA-F0-9]{16}$"),
            ("OSX v10.7", "^[a-fA-F0-9]{136}$"),
            ("OSX v10.8", "^\$ml\$[a-fA-F0-9$]{199}$"),
            ("SAM(LM_Hash:NT_Hash)", "^[a-fA-F0-9]{32}:[a-fA-F0-9]{32}$"),
            ("MSSQL(2000)", "^0x0100[a-f0-9]{0,8}?[a-f0-9]{80}$"),
            (("MSSQL(2005)", "MSSQL(2008)"), "^0x0100[a-f0-9]{0,8}?[a-f0-9]{40}$"),
            ("MSSQL(2012)", "^0x02[a-f0-9]{0,10}?[a-f0-9]{128}$"),
            (("substr(md5($pass),0,16)", "substr(md5($pass),16,16)", "substr(md5($pass),8,16)", "CRC-64"),
             "^[a-fA-F0-9./]{16}$"),
            (("MySQL 4.x", "SHA-1", "HAVAL-160", "SHA-1(MaNGOS)", "SHA-1(MaNGOS2)", "TIGER-160", "RIPEMD-160",
              "RIPEMD-160(HMAC)",
              "TIGER-160(HMAC)", "Skein-256(160)", "Skein-512(160)"), "^[a-f0-9]{40}$"),
            (("SHA-256", "SHA-256(HMAC)", "SHA-3(Keccak)", "GOST R 34.11-94", "RIPEMD-256", "HAVAL-256", "Snefru-256",
              "Snefru-256(HMAC)", "RIPEMD-256(HMAC)", "Keccak-256", "Skein-256", "Skein-512(256)"), "^[a-fA-F0-9]{64}$"),
            (("SHA-1(Oracle)", "HAVAL-192", "OSX v10.4, v10.5, v10.6", "Tiger-192", "TIGER-192(HMAC)"), "^[a-fA-F0-9]{48}$"),
            (("SHA-224", "SHA-224(HMAC)", "HAVAL-224", "Keccak-224", "Skein-256(224)", "Skein-512(224)"), "^[a-fA-F0-9]{56}$"),
            (("Adler32", "FNV-32", "ELF-32", "Joaat", "CRC-32", "CRC-32B", "GHash-32-3", "GHash-32-5", "FCS-32", "Fletcher-32",
              "XOR-32"), "^[a-fA-F0-9]{8}$"),
            (("CRC-16-CCITT", "CRC-16", "FCS-16"), "^[a-fA-F0-9]{4}$"),
            (("MD5(HMAC(Wordpress))", "MD5(HMAC)", "MD5", "RIPEMD-128", "RIPEMD-128(HMAC)", "Tiger-128", "Tiger-128(HMAC)",
              "RAdmin v2.x", "NTLM", "Domain Cached Credentials(DCC)", "Domain Cached Credentials 2(DCC2)", "MD4", "MD2",
              "MD4(HMAC)", "MD2(HMAC)", "Snefru-128", "Snefru-128(HMAC)", "HAVAL-128", "HAVAL-128(HMAC)", "Skein-256(128)",
              "Skein-512(128)", "MSCASH2"), "^[0-9A-Fa-f]{32}$"),
        )

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
                      colour=discord.Colour.red())
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
        if len(message) <= 50:
            hasNums = bool(re.search(r'\d', message))
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
            await ctx.send("```The string may only be up to 50 characters```")

    @deCaeser.error
    async def decaeser_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Please wait {error.retry_after} before using this command")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"```Usage: ./decaesercipher [string]```")
        else:
            await ctx.send("```An unknown error has occured!\nUsage: ./decaesercipher [string]```")
            raise error

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

    @commands.command(name="hashid", description="Identify hashes", aliases=["hashidentifier"])
    async def hashid(self, ctx, hash_=None):
        text = "Usage: ./hashid [hash]"
        if hash_ is None:
            await ctx.send(f"```{text}```")
        else:
            res = []
            for items in self.HASHES:
                if re.match(items[1], hash_):
                    res += [items[0] if isinstance(items[0],str) else items[0]]
            result = ""
            for y in res:
                if isinstance(y, tuple):
                    for x in y:
                        result += f"\n+ {x}"
            await ctx.send(f"""```diff\n{result}```""")


def setup(client):
    client.add_cog(encoding(client))
