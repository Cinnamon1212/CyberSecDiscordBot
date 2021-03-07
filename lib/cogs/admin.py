import discord
from discord.ext import commands

class admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, name="kick", aliases=["kickhammer"], description="Kicks a user from the discord")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if commands.has_permissions(kick_members=True):
            await member.kick(reason=reason)
            await ctx.send(f"{member} has been kicked for {reason}")
        else:
            await ctx.send("You cannot use this command!")
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('I could not find that user')

    @commands.command(pass_context=True, name="ban", aliases=["banhammer"], description="Bans a user from the discord")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str):
        if commands.has_permissions(ban_members=True):
            await member.ban(reason=reason)
            await ctx.send(f"{member} has been banned for {reason}")
        else:
            await ctx.send("You cannot use this command!")
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('I could not find that user')

    @commands.command(pass_context=True, name="clear", aliases=["purge", "remove"], description="Clears messages from a channel")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=1):
        if commands.has_permissions(manage_messages=True):
            await ctx.channel.purge(limit=amount + 1)
        else:
            await ctx.send("You cannot use this command!")

    @commands.command(pass_context=True, name="unban", description="Unbans a user")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        if commands.has_permissions(ban_members=True):
            for ban_entry in banned_users:
                user = ban_entry.user

                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    await ctx.send(f'{user.mention} was unbanned')
                    return
        else:
            await ctx.send('You are not allowed to run that command')

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('I could not find that user')

    @commands.command(name="userinfo", aliases=['user', 'memberinfo'], description="Gathers information on a user")
    async def userinfo(self, ctx, *, member: discord.Member):
        roles = [role for role in member.roles]
        embed = discord.Embed(colour=member.colour, inline=False)
        embed.set_author(name=f"User info for {member}")
        embed.set_thumbnail(url=member.avatar_url)
        time = ctx.message.created_at
        embed.set_footer(text=f"Asked by {ctx.author.name} " + time.strftime("%d/%m/%y %X"))
        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="Guild name: ", value=member.display_name)
        embed.add_field(name="Created at: ", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="Joined at: ", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name=f"Roles ({len(roles)})", value="".join([role.mention for role in roles]))
        embed.add_field(name="Top role:", value=member.top_role.mention)
        embed.add_field(name="Bot?", value=member.bot)
        embed.add_field(name="Flags: ", value=member.public_flags)
        await ctx.send(embed=embed)

    @commands.command(name="serverinfo", aliases=['server', 'guildinfo'], description="Gathers information of the server")
    async def serverinfo(self, ctx):
        name, desc, owner, id, region, membercount, servericon = str(ctx.guild.name), str(ctx.guild.description), str(ctx.guild.owner), str(ctx.guild.id), str(ctx.guild.region), str(ctx.guild.member_count), str(ctx.guild.icon_url)

        embed = discord.Embed(
            title=name + " Server information",
            description=desc,
            colour=discord.Colour.green())
        embed.set_thumbnail(url=servericon)
        embed.add_field(name="Owner:", value=owner, inline=True)
        embed.add_field(name="ID:", value=id, inline=True)
        embed.add_field(name="Region:", value=region, inline=True)
        embed.add_field(name="member count:", value=membercount, inline=True)
        time = ctx.message.created_at
        embed.set_footer(text=f"Asked by {ctx.author.name} " + time.strftime("%d/%m/%y %X"))
        await ctx.send(embed=embed)



def setup(client):
    client.add_cog(admin(client))
