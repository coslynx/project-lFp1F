import discord
from discord.ext import commands
import logging

from database import Database

logging.basicConfig(level=logging.INFO)

class AdminCog(commands.Cog, name="Administration"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = Database()

    @commands.command(name="set_prefix", help="Sets the command prefix for the server.")
    @commands.has_permissions(administrator=True)
    async def set_prefix(self, ctx: commands.Context, prefix: str):
        """Sets the command prefix for the server."""
        self.database.set_server_prefix(ctx.guild.id, prefix)
        await ctx.send(f"Command prefix set to `{prefix}`.")

    @commands.command(name="get_prefix", help="Retrieves the current command prefix for the server.")
    async def get_prefix(self, ctx: commands.Context):
        """Retrieves the current command prefix for the server."""
        prefix = self.database.get_server_prefix(ctx.guild.id)
        await ctx.send(f"Current command prefix is `{prefix}`.")

    @commands.command(name="ban", help="Bans a user from the server.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, member: discord.Member, reason: str = None):
        """Bans a user from the server."""
        try:
            await member.ban(reason=reason)
            await ctx.send(f"Banned {member.name}#{member.discriminator}.")
        except discord.Forbidden:
            await ctx.send(f"I don't have permission to ban {member.name}#{member.discriminator}.")

    @commands.command(name="unban", help="Unbans a user from the server.")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx: commands.Context, user: discord.User, reason: str = None):
        """Unbans a user from the server."""
        try:
            await ctx.guild.unban(user, reason=reason)
            await ctx.send(f"Unbanned {user.name}#{user.discriminator}.")
        except discord.Forbidden:
            await ctx.send(f"I don't have permission to unban {user.name}#{user.discriminator}.")

    @commands.command(name="kick", help="Kicks a user from the server.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, member: discord.Member, reason: str = None):
        """Kicks a user from the server."""
        try:
            await member.kick(reason=reason)
            await ctx.send(f"Kicked {member.name}#{member.discriminator}.")
        except discord.Forbidden:
            await ctx.send(f"I don't have permission to kick {member.name}#{member.discriminator}.")

    @commands.command(name="add_role", help="Assigns a role to a user.")
    @commands.has_permissions(manage_roles=True)
    async def add_role(self, ctx: commands.Context, member: discord.Member, role: discord.Role):
        """Assigns a role to a user."""
        try:
            await member.add_roles(role)
            await ctx.send(f"Added role {role.name} to {member.name}#{member.discriminator}.")
        except discord.Forbidden:
            await ctx.send(f"I don't have permission to add roles to {member.name}#{member.discriminator}.")

    @commands.command(name="remove_role", help="Removes a role from a user.")
    @commands.has_permissions(manage_roles=True)
    async def remove_role(self, ctx: commands.Context, member: discord.Member, role: discord.Role):
        """Removes a role from a user."""
        try:
            await member.remove_roles(role)
            await ctx.send(f"Removed role {role.name} from {member.name}#{member.discriminator}.")
        except discord.Forbidden:
            await ctx.send(f"I don't have permission to remove roles from {member.name}#{member.discriminator}.")

    @commands.command(name="set_channel", help="Sets a specific channel for bot actions.")
    @commands.has_permissions(administrator=True)
    async def set_channel(self, ctx: commands.Context, channel: discord.TextChannel, action: str):
        """Sets a specific channel for bot actions."""
        if action.lower() not in ["music", "log"]:
            await ctx.send(f"Invalid action. Please use 'music' or 'log'.")
            return

        self.database.set_server_channel(ctx.guild.id, action, channel.id)
        await ctx.send(f"Set {action} channel to {channel.mention}.")

    @commands.command(name="reload_cogs", help="Reloads all the bot's cogs.")
    @commands.has_permissions(administrator=True)
    async def reload_cogs(self, ctx: commands.Context):
        """Reloads all the bot's cogs."""
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    self.bot.reload_extension(f'cogs.{filename[:-3]}')
                    await ctx.send(f"Reloaded cog: {filename[:-3]}.")
                except Exception as e:
                    await ctx.send(f"Failed to reload cog {filename[:-3]}: {e}")

    @commands.command(name="shutdown", help="Shuts down the bot gracefully.")
    @commands.is_owner()  # Ensure only the bot owner can use this command
    async def shutdown(self, ctx: commands.Context):
        """Shuts down the bot gracefully."""
        await ctx.send("Shutting down...")
        await self.bot.close()

def setup(bot: commands.Bot):
    bot.add_cog(AdminCog(bot))