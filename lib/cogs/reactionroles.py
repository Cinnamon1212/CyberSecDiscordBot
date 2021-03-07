import discord
from discord.ext import commands
import aiofiles
class reactroles(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        self.client.reaction_roles = []

        for file in ["reactionroles.txt"]:
            async with aiofiles.open(file, mode="a") as temp:
                pass
        async with aiofiles.open("reactionroles.txt", mode="r") as file:
            lines = await file.readlines()
            for line in lines:
                data = line.split("")
                self.client.reaction_roles.append((int(data[0]), int(data[1]), data[2].strip("\n")))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        for role_id, msg_id, emoji in self.client.reaction_roles:
            if msg_id == payload.message_id and emoji == str(payload.emoji.name.encode("utf-8")):
                await payload.member.add_roles(self.client.get_guild(payload.guild_id).get_role(role_id))
                return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        for role_id, msg_id, emoji in self.client.reaction_roles:
            if msg_id == payload.message_id and emoji == str(payload.emoji.name.encode("utf-8")):
                guild = self.client.get_guild(payload.guild_id)
                await guild.get_member(payload.user_id).remove_roles(guild.get_role(role_id))
                return

    @commands.command()
    async def set_reaction(self, ctx, role: discord.Role = None, msg: discord.Message = None, emoji=None):
        if role is not None and msg is not None and emoji is not None:
            await msg.add_reaction(emoji)
            self.client.reaction_roles.append((role, msg, str(emoji.encode("utf-8"))))

            async with aiofiles.open("reactionroles.txt", mode="a") as file:
                emoji_utf = emoji.encode("utf-8")
                await file.write(f"{role.id} {msg.id} {emoji_utf}\n")
            await ctx.channel.send("Reaction has been sent")
        else:
            if role is None:
                await ctx.send("Please provide a role")
            elif msg is None:
                await ctx.send("Please provide a message")
            elif emoji is None:
                await ctx.send("Please provide an emoji")
            else:
                await ctx.send("Invalid args!")
def setup(client):
    client.add_cog(reactroles(client))
