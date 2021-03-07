import discord, math, re
from discord.ext import commands
from discord import Embed

def syntax(command):
    cmd_and_aliases = "|".join([str(command), *command.aliases])
    params = []

    for key, value in command.params.items():
        if key not in ("self", "ctx"):
            params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")

    params = " ".join(params)
    return f"`{cmd_and_aliases} {params}`"

class help(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.remove_command('help')

    @commands.command(name="help", aliases=["commands", "h"], description="Displays this command")
    async def help(self, ctx, cog="1"):
        embed = Embed(title="Command help",
                      description="A list of commands and how to use them!",
                      colour=ctx.author.colour)
        embed.set_thumbnail(url=self.client.user.avatar_url)

        cogs = [c for c in self.client.cogs.keys()]
        totalPages = math.ceil(len(cogs) / 4)

        if re.search(r"\d", str(cog)):
            cog = int(cog)
            if cog > totalPages or cog < 1:
                await ctx.send(f"Invalid page number: {cog} Please pick from {totalPages} pages or with no args.")
                return

            embed.set_footer(text=f"Page {cog} of {totalPages}")

            neededCogs = []
            for i in range(4):
                x = i + (int(cog) - 1) * 4
                try:
                    neededCogs.append(cogs[x])
                except IndexError:
                    pass
            for cog in neededCogs:
                commandList = ""
                for command in self.client.get_cog(cog).walk_commands():
                    if command.hidden:
                        continue
                    elif command.parent is not None:
                        continue
                    commandList += f"**{command.name}** - *{command.description}** -  Format:** {syntax(command)}*\n\n"
                commandList += "\n"

                embed.add_field(name=cog, value=commandList, inline=False)

        elif re.search(r"a-zA-Z", str(cog)):
            lowerCogs = [c.lower() for c in cogs]
            if cog.lower() not in lowerCogs:
                await ctx.send(f"Invalid arg: {cog}, please pick from page {totalPages}")
                return

            embed.set_footer(
                text=f"Cog {(lowerCogs.index(cog.lower())+1)} of {len(lowerCogs)}. [] Optional, <> Required.")

            helpText = ""

            for command in self.client.get_cog(cogs[lowerCogs.index(cog.lower())]).walk_commands():
                if command.hidden:
                    continue

                elif command.parent is None:
                    continue

                helpText += f"```{command.name}```\n**{command.description}**\n Format:** {syntax(command)}"

        else:
            await ctx.send(f"Invalid argument: `{cog}`\nPlease pick from {totalPages} pages.")
            return
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(help(client))
