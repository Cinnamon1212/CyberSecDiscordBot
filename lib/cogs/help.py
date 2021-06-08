import discord, math, re
from discord.ext import commands
from discord import Embed
from pygicord import Paginator

def syntax(command):
    cmd_and_aliases = "|".join([str(command), *command.aliases])
    params = []

    for key, value in command.params.items():
        if key not in ("self", "ctx"):
            params.append(f"({key})" if "NoneType" in str(value) else f"[{key}]")

    params = " ".join(params)
    return f"`{cmd_and_aliases} {params}`"

class help(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.remove_command('help')

    @commands.command(name="help", aliases=["commands", "h"], description="Displays this command")
    async def help(self, ctx):
        pages = []
        # MAIN MENU
        main = Embed(title="Command help", colour=discord.Colour.random())
        main.add_field(name="```(1) Main```", value="Main page", inline=False)
        main.add_field(name="```(2) Network and hacking utilities```", value="Networking and hacking utilities", inline=False)
        main.add_field(name="```(3) Website and cryptography utlities```", value="Website and encoding utilities")
        main.add_field(name="```(4) Recourses```", value="A list of programming and hacking recourses", inline=False)
        main.add_field(name="```(5) OSINT```", value="OSINT Utilities")
        main.add_field(name="```(6) Administration```", value="General administration commands", inline=False)
        main.add_field(name="```(7) Maths```", value="Math utilities", inline=False)
        main.add_field(name="```(8) Conversions```", value="Different types of converters", inline=False)
        main.add_field(name="```(9) Fun ```", value="Some fun commands", inline=False)
        main.add_field(name="```(10) AI```", value="Commands using AI", inline=False)
        main.add_field(name="```(11) Misc```", value="Bot information and commands without a category", inline=False)
        main.set_footer(text="Please use the 🔢 button to jump to a page (page 1 out of 11)")
        pages.append(main)

        # HACKING AND NETWORKING UTILS
        utils = Embed(title="Networking and hacking utilities", colour=discord.Colour.random())
        for command in self.client.get_cog("networkingtools").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            else:
                utils.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)
        for command in self.client.get_cog("shodan").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            else:
                utils.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)
        utils.set_footer(text="Please use the 🔢 button to jump to a page (page 2 out of 11)")
        pages.append(utils)

        # WEBSITE AND CRYPTO UTILS
        web = Embed(title="Website and cryptography utilities", colour=discord.Colour.random())
        for command in self.client.get_cog("websites").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            else:
                web.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)
        web.set_footer(text="Please use the 🔢 button to jump to a page (page 3 out of 11)")
        for command in self.client.get_cog("encoding").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            else:
                web.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)
        pages.append(web)

        # RECOURSES
        recourses = Embed(title="Recourses", colour=discord.Colour.random())
        for command in self.client.get_cog("recourses").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            else:
                recourses.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)
        recourses.set_footer(text="Please use the 🔢 button to jump to a page (page 4 out of 11)")
        pages.append(recourses)

        # OSINT
        OSINT = Embed(title="OSINT utilities", colour=discord.Colour.random())
        for command in self.client.get_cog("osint").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            else:
                OSINT.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)
        OSINT.set_footer(text="Please use the 🔢 button to jump to a page (page 5 out of 11)")
        pages.append(OSINT)

        # ADMIN
        admin = Embed(title="General administration commands", colour=discord.Colour.random())
        for command in self.client.get_cog("admin").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            else:
                admin.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)
        admin.set_footer(text="Please use the 🔢 button to jump to a page (page 6 out of 11)")
        pages.append(admin)

        # MATHS
        maths = Embed(title="Math utilities", colour=discord.Colour.random())
        for command in self.client.get_cog("maths").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            else:
                maths.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)
        maths.set_footer(text="Please use the 🔢 button to jump to a page (page 7 out of 11)")
        pages.append(maths)

        # CONVERSIONS
        conversions = Embed(title="Different types of converters", colour=discord.Colour.random())
        for command in self.client.get_cog("conversions").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            else:
                conversions.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)
        conversions.set_footer(text="Please use the 🔢 button to jump to a page (page 8 out of 11)")
        pages.append(conversions)

        # FUN
        fun = Embed(title="Some fun commands", colour=discord.Colour.random())
        for command in self.client.get_cog("fun").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            else:
                fun.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)
        fun.set_footer(text="Please use the 🔢 button to jump to a page (page 9 out of 11)")
        pages.append(fun)

        # AI
        AI = Embed(title="Commands that use AI", colour=discord.Colour.random())
        for command in self.client.get_cog("AI").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            else:
                AI.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)
        AI.set_footer(text="Please use the 🔢 button to jump to a page (page 10 out of 11)")
        pages.append(AI)

        # MISC
        misc = Embed(title="Bot information and commands without a category", colour=discord.Colour.random())
        for command in self.client.get_cog("misc").walk_commands():
            if command.hidden:
                continue
            elif command.parent is not None:
                continue
            else:
                misc.add_field(name=f"**{command.name}**", value=f"{command.description} - Format: {syntax(command)}", inline=False)
        misc.set_footer(text="Please use the 🔢 button to jump to a page (page 11 out of 11)")
        pages.append(misc)

        paginator = Paginator(pages=pages)
        await paginator.start(ctx)
def setup(client):
    client.add_cog(help(client))
