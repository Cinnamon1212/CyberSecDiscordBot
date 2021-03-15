import discord, os
from bs4 import BeautifulSoup as soup
from discord.ext import commands
from discord import Embed
from urllib.request import urlopen as uReq

class recourses(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="ParrotOSDownloads", description="List of parrot OS downloads", aliases=["ParrotOS", "ParrotDownload", "dlParrot"])
    async def downloadparrotOS(self, ctx, *, version: str):
        url = "https://www.parrotsec.org/download/"
        uClient = uReq(url)
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html, "html.parser")
        downloads_location = page_soup.find_all("div", {"style": "margin: 2em;padding: 2em;background-color:#30363D"})
        links = []
        for download in downloads_location:
            links.append(download.find_all("a"))

        if version.lower() == "home mate" or version.lower() == "mate home":
            embed = Embed(title="Downloads for Parrot OS (Home Mate): ",
                          url="https://www.parrotsec.org/",
                          colour=discord.Colour.random())
            embed.set_thumbnail(url="https://parrotsec.org/images/logo.png")
            home_mate_links = []
            for link in links[0]:
                home_mate_links.append(link["href"])
            embed.add_field(name="Direct download: ", value=f"{home_mate_links[0]}", inline=False)
            embed.add_field(name="Mirror download: ", value=f"{home_mate_links[1]}", inline=False)
            embed.add_field(name="Torrent download: ", value=f"{home_mate_links[2]}", inline=False)
            await ctx.send(embed=embed)

        elif version.lower() == "kde mate" or version.lower() == "kde home":
            embed = Embed(title="Downloads for Parrot OS (Home KDE): ",
                          url="https://www.parrotsec.org/",
                          colour=discord.Colour.random())
            embed.set_thumbnail(url="https://parrotsec.org/images/logo.png")
            home_KDE_links = []
            for link in links[1]:
                home_KDE_links.append(link["href"])
            embed.add_field(name="Direct download: ", value=f"{home_KDE_links[0]}", inline=False)
            embed.add_field(name="Mirror download: ", value=f"{home_KDE_links[1]}", inline=False)
            embed.add_field(name="Torrent download: ", value=f"{home_KDE_links[2]}", inline=False)
            await ctx.send(embed=embed)

        elif version.lower() == "mate ova" or version.lower() == "ova mate":
            embed = Embed(title="Downloads for Parrot OS (Home Mate OVA): ",
                          url="https://www.parrotsec.org/",
                          colour=discord.Colour.random())
            embed.set_thumbnail(url="https://parrotsec.org/images/logo.png")
            home_Mate_Ova_links = []
            for link in links[2]:
                home_Mate_Ova_links.append(link["href"])
            embed.add_field(name="Direct download: ", value=f"{home_Mate_Ova_links[0]}", inline=False)
            embed.add_field(name="Mirror download: ", value=f"{home_Mate_Ova_links[1]}", inline=False)
            embed.add_field(name="Torrent download: ", value=f"{home_Mate_Ova_links[2]}", inline=False)
            await ctx.send(embed=embed)

        elif version.lower() == "security mate" or version.lower() == "mate security":
            embed = Embed(title="Downloads for Parrot OS (Mate Security): ",
                          url="https://www.parrotsec.org/",
                          colour=discord.Colour.random())
            embed.set_thumbnail(url="https://parrotsec.org/images/logo.png")
            Mate_Security_links = []
            for link in links[3]:
                Mate_Security_links.append(link["href"])
            embed.add_field(name="Direct download: ", value=f"{Mate_Security_links[0]}", inline=False)
            embed.add_field(name="Mirror download: ", value=f"{Mate_Security_links[1]}", inline=False)
            embed.add_field(name="Torrent download: ", value=f"{Mate_Security_links[2]}", inline=False)
            await ctx.send(embed=embed)

        elif version.lower() == "security kde" or version.lower() == "kde security":
            embed = Embed(title="Downloads for Parrot OS (KDE Security): ",
                          url="https://www.parrotsec.org/",
                          colour=discord.Colour.random())
            embed.set_thumbnail(url="https://parrotsec.org/images/logo.png")
            KDE_Security_links = []
            for link in links[4]:
                KDE_Security_links.append(link["href"])
            embed.add_field(name="Direct download: ", value=f"{KDE_Security_links[0]}", inline=False)
            embed.add_field(name="Mirror download: ", value=f"{KDE_Security_links[1]}", inline=False)
            embed.add_field(name="Torrent download: ", value=f"{KDE_Security_links[2]}", inline=False)
            await ctx.send(embed=embed)

        elif version.lower() == "security ova" or version.lower() == "ova security":
            embed = Embed(title="Downloads for Parrot OS (Mate Security OVA): ",
                          url="https://www.parrotsec.org/",
                          colour=discord.Colour.random())
            embed.set_thumbnail(url="https://parrotsec.org/images/logo.png")
            Security_OVA = []
            for link in links[5]:
                Security_OVA.append(link["href"])
            embed.add_field(name="Direct download: ", value=f"{Security_OVA[0]}", inline=False)
            embed.add_field(name="Mirror download: ", value=f"{Security_OVA[1]}", inline=False)
            embed.add_field(name="Torrent download: ", value=f"{Security_OVA[2]}", inline=False)
            await ctx.send(embed=embed)

        else:
            await ctx.send("Please choose from: Mate home, KDE Home, Mate OVA, Security Mate, Security KDE and Security OVA ")

    @downloadparrotOS.error
    async def parrotos_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please choose from: Mate home, KDE Home, Mate OVA, Security Mate, Security KDE and Security OVA ")
        else:
            raise


def setup(client):
    client.add_cog(recourses(client))
