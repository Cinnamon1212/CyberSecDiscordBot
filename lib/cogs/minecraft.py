import discord, os, requests, json
from discord.ext import commands
from mcstatus import MinecraftServer
from discord import Embed
from aiohttp import request
class minecraft(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="minecraftstatus", aliases=["serverlookup", "mcserver", "mlookup"], description="Returns status of a minecraft server")
    async def minecraftstatus(self, ctx, mineserver):
        URL = "https://api.mcsrvstat.us/2/" + mineserver
        async with request("GET", URL, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                if data['ip'] == "":
                    await ctx.send("Server not found!")
                else:
                    if data['online'] is not False:
                        server = MinecraftServer.lookup(mineserver)
                        status = server.status()
                        ip = str(data['ip'])
                        motd = data['motd']['clean']
                        players = data['players']['online']
                        if 0 < players:
                            plist = data['players']['list']
                        else:
                            plist = "No players online"
                        mcport = data['port']
                        mcversion = data['version']
                        online = data['online']
                        embed = Embed(title=data["ip"],
                                      description=str(motd),
                                      colour=discord.Colour.random(),
                                      inline=False)
                        embed.set_thumbnail(url=f"https://api.minetools.eu/favicon/{ip}/{mcport}")
                        embed.add_field(name="Players online: ", value=str(players))
                        embed.add_field(name="Player list: ", value=str(plist))
                        embed.add_field(name="Version: ", value=str(mcversion))
                        embed.add_field(name="Ping: ", value=f"{status.latency}")
                        embed.add_field(name="Online: ", value=online)
                        embed.add_field(name="Port: ", value=str(mcport))
                        embed.set_footer(text=f"Asked by {ctx.author.name}")
                        await ctx.send(embed=embed)
                        print(status.latency)
            else:
                await ctx.send("API error")
                print(f" API returned {response.status}")

    @minecraftstatus.error
    async def mcstatus_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please provide a server")

    @commands.command(name="mcplayer", aliases=["Playerlookup", "plookup"], description="Returns information on a minecraft player")
    async def mcplayer(self, ctx, playername):
        GrabUUID = "https://api.minetools.eu/uuid/" + playername
        async with request("GET", GrabUUID, headers={}) as uuidresponse:
            if uuidresponse.status == 200:
                data = await uuidresponse.json()
                uuid = data['id']
                if uuid is not None:
                    URL = "https://api.minetools.eu/profile/" + uuid
                    async with request("GET", URL, headers={}) as response:
                        if response.status == 200:
                            data = await response.json()

                            profilename = data['decoded']['profileName']
                            skin = data['decoded']['textures']['SKIN']['url']
                            profileid = data['decoded']['profileId']
                            signaturereq = data['decoded']['signatureRequired']
                            embed = Embed(title=f"Information on player: {profilename}",
                                          description=f"Profile ID: {profileid}")
                            embed.add_field(name="Signature required", value=signaturereq)
                            embed.set_thumbnail(url=skin)
                            embed.set_footer(text=f"Asked by {ctx.author.name}")
                            await ctx.send(embed=embed)
                        else:
                            await ctx.send("Server gave no response, please ensure you provide a player UUID")
                            print(f"API returned {response.status}")
                else:
                    await ctx.send("User not found!")
            else:
                await ctx.send("API Error")
                print(f"API returned {response.status}")

    @mcplayer.error
    async def mcplayer_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please provide a minecraft player")
        else:
            raise




def setup(client):
    client.add_cog(minecraft(client))
