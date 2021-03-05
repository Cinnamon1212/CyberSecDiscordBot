# Credits to the The-Black-Knights
# Author: R37r0-Gh057
# Idea: Yuma-Tsushima
from discord.ext import commands
import discord

class Administration(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(
		name='kick',
		description='the kick command',
		aliases=['k']
		)
	async def kick(self,ctx,member:discord.Member,*,reason=None):
		await member.kick(reason=reason)
		await ctx.send(f'{member.mention} has been kicked. REASON: "{reason}"')
		return
	@commands.command(
		name='ban',
		description='the ban command',
		aliases=['obliterate']
		)
	async def ban(self,ctx,member:discord.Member,*,reason=None):
		await member.ban(reason=reason)
		await ctx.send(f'{member.mention} has been banned. REASON: "{reason}"')
		return
	@commands.command(
		name='unban',
		description='the unban command',
		aliases=['revive']
		)
	async def revive(self,ctx,*,member):
		found = False
		obliterated = await ctx.guild.bans()
		human_name, human_disc = member.split('#')
		for human in obliterated:
			user = human.user

			if (user.name, user.discriminator) == (human_name,human_disc):
				await ctx.guild.unban(user)
				await ctx.send(f'{user.mention} has been revived.')
				found = True
				return
			if not found:
				await ctx.send(f'{user.mention} is not in the ban list.')
				return
	@commands.command(
		name='purge',
		description='the purge command',
		aliases=['clean']
		)
	async def purge(self,ctx,amount=10):
		await ctx.channel.purge(limit=amount+1)
		return

def setup(client):
	client.add_cog(Administration(client))
