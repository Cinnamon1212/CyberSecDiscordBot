import discord, asyncio
from discord.ext import commands

class admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="kick", description="Kicks a discord user", aliases=["kickhammer"])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Unspecified reason"):
        text = "Usage: ./kick [member] (reason)"
        if member is None:
            await ctx.send(f"```{text}```")
        else:
            bot_ = ctx.guild.get_member(self.client.user.id)
            author = ctx.guild.get_member(ctx.author.id)
            if member.top_role > author.top_role:
                await ctx.send("This user has higher permissions than you!")
            elif bot_.top_role < member.top_role:
                await ctx.send("The user has higher permissions than I do!")
            else:
                await member.kick(reason=reason)
                await ctx.send(f"{member.name} was kicked for {reason}")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            text = "Usage: ./kick [member] (reason)"
            await ctx.send(f"```You do not have sufficient permissions to use this command\n{text}```")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"```An error has occured, likely the bot is missing permissions\n{text}```")
        else:
            raise

    @commands.command(name="ban", description="bans a discord user", aliases=["banhammer"])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, *, reason="Unspecified reason"):
        text = "Usage: ./ban [member] (reason)"
        if member is None:
            await ctx.send(f"```{text}```")
        else:
            bot_ = ctx.guild.get_member(self.client.user.id)
            author = ctx.guild.get_member(ctx.author.id)
            if member.top_role > author.top_role:
                await ctx.send("This user has higher permissions than you!")
            elif bot_.top_role < member.top_role:
                await ctx.send("The user has higher permissions than I do!")
            else:
                await member.ban(reason=reason)
                await ctx.send(f"{member.name} was banned for {reason}")

    @ban.error
    async def ban_error(self, ctx, error):
        text = "Usage: ./ban [member] (reason)"
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"```You do not have sufficient permissiosn to use this command\n{text}```")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"```An error has occured, likely the bot is missing permissions\n{text}```")
        else:
            raise

    @commands.command(name="unban", description="unbans a discord user", aliases=["unbanhammer"])
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        text = "Usage: ./unban [member/ID]"
        if len(member) == 18:
            try:
                member = int(member)
                user = self.client.fetch_user
                await ctx.guild.unban(user)
                stop = True
            except discord.NotFound:
                await ctx.send(f"```Unable to find a user with the provided ID!\n{text}```")
                stop = True
        else:
            stop = False
        if stop is False:
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split('#')
            for banned in banned_users:
                x = banned.user
                if (x.name, x.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(x)
                    await ctx.send(f"```{x.name}#{x.discriminator} has been unbanned```")

    @unban.error
    async def unban_error(self, ctx, error):
        text = "Usage: ./unban [member/ID]"
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"```You do not have sufficient permissiosn to use this command\n{text}```")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"```An error has occured, likely the bot is missing permissions\n{text}```")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"```{text}```")
        else:
            raise

    @commands.command(pass_context=True, name="clear", aliases=["purge", "remove"], description="Clears messages from a channel")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=1, channel_id=None):
        text = """Usage: ./clear [Amount/ID] (channel)
if the command is not in the channel, please specify the channel"""
        if commands.has_permissions(manage_messages=True):
            if len(str(amount)) != 18:
                try:
                    amount = int(amount)
                    check = True
                except ValueError:
                    await ctx.send(f"```Invalid amount of numbers\n{text}```")
                    check = False
                if check is True:
                    if amount > 50:
                        if ctx.author.top_role.permissions.administrator is True:
                            await ctx.send(f"You are about to delete {amount} message, are you sure you'd like to continue (Y/N)?")
                            accepted = ["yes", "no", "y", "n"]
                            try:
                                confirm = await self.client.wait_for(
                                            "message",
                                            timeout=20,
                                            check=lambda message: message.author == ctx.author and message.channel == ctx.channel and message.content.lower() in accepted)
                            except asyncio.TimeoutError:
                                await ctx.send("Clear command timed out", delete_after=10)
                            positives = ["yes", "y"]
                            negatives = ["no", "n"]
                            if confirm.content.lower() in positives:
                                await ctx.channel.purge(limit=amount + 1)
                            elif confirm.content.lower() in negatives:
                                await ctx.send("Clear command was cancelled", delete_after=10)
                        else:
                            await ctx.send(f"```Mass clearing is limited to Administrators only!\n{text}```")
                    else:
                        await ctx.channel.purge(limit=amount + 1)
            else:
                try:
                    messageid = int(amount)
                    check = True
                except ValueError:
                    await ctx.send(f"```Invalid message ID\n{text}```")
                    check = False
                if check is True:
                    if channel_id is None:
                        msg = await ctx.channel.fetch_message(messageid)
                        await msg.delete()
                        await ctx.send("```Message deleted```", delete_after=10)
                    else:
                        if len(str(channel_id)) == 18:
                            try:
                                channel_id = int(channel_id)
                                check = True
                            except ValueError:
                                await ctx.send(f"```Invalid channel ID\n{text}```")
                            for channel in ctx.guild.channels:
                                if channel.id == channel_id:
                                    message_channel = channel
                                    break
                                else:
                                    message_channel = None
                            if message_channel is not None:
                                msg = await message_channel.fetch_message(messageid)
                                await msg.delete()
                                await ctx.send("```Message deleted```", delete_after=10)
                            else:
                                await ctx.send(f"```Unable to find channel\n{text}```")
        else:
            await ctx.send(f"```You do not have sufficient permissions\n{text}```")

    @clear.error
    async def clear_error(self, ctx, error):
        text = """Usage: ./clear [Amount/ID] (channel)
if the command is not in the channel, please specify the channel"""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"```You do not have sufficient permissions\n{text}```")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("An error has occured, likely the bot is missing permissions")
        else:
            raise


    @commands.command(name="userinfo", aliases=['user', 'memberinfo'], description="Gathers information on a user")
    async def userinfo(self, ctx, *, member: discord.Member=None):
        text = "Usage: ./userinfo [member]"
        try:
            roles = [role for role in member.roles]
        except AttributeError:
            await ctx.send(f"```{text}```")
        else:
            embed = discord.Embed(colour=member.colour)
            embed.set_author(name=f"User info for {member}")
            embed.set_thumbnail(url=member.avatar_url)
            time = ctx.message.created_at
            embed.set_footer(text=f"Asked by {ctx.author.name} " + time.strftime("%d/%m/%y %X"))
            embed.add_field(name="ID:", value=member.id, inline=False)
            embed.add_field(name="Guild name: ", value=member.display_name, inline=False)
            embed.add_field(name="Created at: ", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)
            embed.add_field(name="Joined at: ", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)
            embed.add_field(name=f"Roles ({len(roles)})", value="".join([role.mention for role in roles]), inline=False)
            embed.add_field(name="Top role:", value=member.top_role.mention, inline=False)
            embed.add_field(name="Bot?", value=member.bot, inline=False)
            await ctx.send(embed=embed)

    async def userinfo_error(self, ctx, error):
        text = "Usage: ./userinfo [member]"
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(f"```User not found\n{text}```")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"```{text}```")


    @commands.command(name="serverinfo", aliases=['server', 'guildinfo'], description="Gathers information of the server")
    async def serverinfo(self, ctx):
        if ctx.guild.description is None:
            desc = "this server has no description"
        else:
            desc = ctx.guild.description
        embed = discord.Embed(
            title=f"{ctx.guild.name} information",
            description=desc,
            colour=discord.Colour.random())
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.add_field(name="ID: ", value=ctx.guild.id, inline=False)
        embed.add_field(name="Region: ", value=ctx.guild.region, inline=False)
        embed.add_field(name="Member count: ", value=f"This server has {ctx.guild.member_count} members", inline=False)
        embed.add_field(name="Roles: ", value=f"This server has {len(ctx.guild.roles) - 1} roles", inline=False)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        time = ctx.message.created_at
        embed.set_footer(text=f"Asked by {ctx.author.name} " + time.strftime("%d/%m/%y %X"))
        await ctx.send(embed=embed)

    @serverinfo.error
    async def serverinfo_error(self, ctx, error):
        await ctx.send(f"""```An error has occured while running the command.
Please ensure this is ran within the context of a server/guild\nUsage: ./serverinfo```""")


    @commands.command(name="rolemod", description="Add/Remove a role to a user", aliases=["giverole", "addrole", "remrole"])
    @commands.has_permissions(manage_roles=True)
    async def rolemod(self, ctx, method, member: discord.Member, role: discord.Role):
        text = "Usage: ./rolemod [add/remove] [member] [role]"
        if method.lower() == "add":
            if role in member.roles:
                await ctx.send(f"```The user already has this role\n{text}```")
            else:
                await member.add_roles(role)

        elif method.lower() in ["rem", "remove", "del"]:
            if role not in member.roles:
                await ctx.send(f"```The user doesn't have {role.name}\n{text}```")
            else:
                bot_ = ctx.guild.get_member(self.client.user.id)
                if bot_.top_role < member.top_role:
                    await ctx.send(f"```This user has higher permissions than I do\n{text}```")
                elif ctx.author.top_role < member.top_role:
                    await ctx.send(f"```This user has higher permissions than you do\n{text}```")
                else:
                    await member.remove_roles(role)

    @rolemod.error
    async def rolemod_error(self, ctx, error):
        text = "Usage: ./rolemod [method] [member] [role]"
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"```You do not have permissions to run this command\n{text}```")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(f"```Member not found\n{text}```")
        elif isinstance(error, commands.RoleNotFound):
            await ctx.send(f"```Role not found\n{text}```")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"```{text}```")
        else:
            raise



def setup(client):
    client.add_cog(admin(client))
