import discord, math, re
from discord.ext import commands
from discord import Embed
from dpymenus import Page, PaginatedMenu

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
    @commands.bot_has_permissions(manage_messages=True)
    async def help(self, ctx):
        menu = PaginatedMenu(ctx)

        page1 = Page(title="Comamnd help", description="Please use ./help (cog) for help on commands within a cog!", colour=discord.Colour.random())
        page1.add_field(name="Utility tools: ", value="Networking, website and hacking tools", inline=False)
        page1.add_field(name="Recourses: ", value="A list of programming and hacking recourses", inline=False)
        page1.add_field(name="AI: ", value="Commands using AI")
        page1.add_field(name="Music: ", value="Music commands and song lyrics", inline=False)
        page1.add_field(name="Administration: ", value="General administration commands", inline=False)
        page1.add_field(name="Maths: ", value="Various maths commands", inline=False)
        page1.add_field(name="Fun: ", value="Fun and off-topic commands", inline=False)
        page1.add_field(name="Misc: ", value="Bot information or commands without category", inline=False)

        page2 = Page(title="Utility tools pt1", description = "Networking and hacking tools", inline=False, colour=discord.Colour.random())
        for command in self.client.get_cog("networkingtools").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            page2.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)
        for command in self.client.get_cog("shodan").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            page2.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)

        page3 = Page(title="Utility tools pt2", description = "Website and cryptography tools", inline=False, colour=discord.Colour.random())
        for command in self.client.get_cog("websites").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            page3.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)
        for command in self.client.get_cog("encoding").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            page3.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)

        page4 = Page(title="AI", description="Commands using AI", inline=False, colour=discord.Colour.random())
        for command in self.client.get_cog("AI").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            page4.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)

        page5 = Page(title="Recourses", description="A list of programming and hacking recourses", inline=False, colour=discord.Colour.random())
        for command in self.client.get_cog("recourses").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            page5.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)
        for command in self.client.get_cog("googleapi").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            page5.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)

        page6 = Page(title="Music", description="Music commands and song lyrics", inline=False, colour=discord.Colour.random())
        for command in self.client.get_cog("music").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            page6.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)

        page7 = Page(title="Administration", description="General administration commands", inline=False, colour=discord.Colour.random())
        for command in self.client.get_cog("admin").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            page7.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)
        for command in self.client.get_cog("reactroles").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            page7.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)

        page8 = Page(title="Maths", description="Various maths commands", inline=False, colour=discord.Colour.random())
        for command in self.client.get_cog("maths").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            page8.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)

        page9 = Page(title="Fun pt1", description="Fun and off-topic commands", inline=False, colour=discord.Colour.random())
        for command in self.client.get_cog("fun").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            page9.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)
        for command in self.client.get_cog("minecraft").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            page9.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)

        page10 = Page(title="Fun pt2", description="Fun and off-topic commands", inline=False, colour=discord.Colour.random())
        for command in self.client.get_cog("reddit_commands").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            page10.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)

        page11 = Page(title="Misc", description="Bot information or commands without catergory", inline=False, colour=discord.Colour.random())
        for command in self.client.get_cog("misc").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            page11.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)

        pages = [page1, page2, page3, page4, page5, page6, page7, page8, page9, page10, page11]
        menu.add_pages(pages)
        menu.set_timeout(180)
        menu.show_skip_buttons()
        menu.show_page_numbers()

        await menu.open()

    @help.error
    async def help_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send("Bot is missing the manage messages permission")
        else:
            raise




def setup(client):
    client.add_cog(help(client))
