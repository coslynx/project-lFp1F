import discord
from discord.ext import commands
import logging

logging.basicConfig(level=logging.INFO)

class UtilityCog(commands.Cog, name="Utilities"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ping", help="Check if the bot is alive and responsive.")
    async def ping(self, ctx: commands.Context):
        """Checks the bot's latency and responds with the ping."""
        await ctx.send(f"Pong! Latency: {round(self.bot.latency * 1000)}ms")

    @commands.command(name="get_user", help="Get information about a user by mentioning them.")
    async def get_user(self, ctx: commands.Context, user: discord.Member):
        """Retrieves user information and displays it in a formatted message."""
        embed = discord.Embed(title=f"User Information - {user.name}", color=discord.Color.blue())
        embed.add_field(name="Username", value=user.name, inline=True)
        embed.add_field(name="Discriminator", value=user.discriminator, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Top Role", value=user.top_role.name, inline=True)
        embed.add_field(name="Joined Server At", value=user.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.set_thumbnail(url=user.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name="get_channel", help="Get information about a channel by mentioning it.")
    async def get_channel(self, ctx: commands.Context, channel: discord.TextChannel):
        """Retrieves channel information and displays it in a formatted message."""
        embed = discord.Embed(title=f"Channel Information - {channel.name}", color=discord.Color.blue())
        embed.add_field(name="Channel Name", value=channel.name, inline=True)
        embed.add_field(name="Channel ID", value=channel.id, inline=True)
        embed.add_field(name="Channel Type", value=channel.type, inline=True)
        embed.add_field(name="Created At", value=channel.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        embed.add_field(name="Category", value=channel.category.name if channel.category else "N/A", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="get_role", help="Get information about a role by mentioning it.")
    async def get_role(self, ctx: commands.Context, role: discord.Role):
        """Retrieves role information and displays it in a formatted message."""
        embed = discord.Embed(title=f"Role Information - {role.name}", color=discord.Color.blue())
        embed.add_field(name="Role Name", value=role.name, inline=True)
        embed.add_field(name="Role ID", value=role.id, inline=True)
        embed.add_field(name="Role Color", value=role.color, inline=True)
        embed.add_field(name="Role Position", value=role.position, inline=True)
        embed.add_field(name="Members", value=len(role.members), inline=True)
        embed.add_field(name="Hoisted", value=role.hoist, inline=True)
        embed.add_field(name="Mentionable", value=role.mentionable, inline=True)
        embed.add_field(name="Created At", value=role.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="parse_args", help="Demonstrates argument parsing.")
    async def parse_args(self, ctx: commands.Context, *args):
        """Parses arguments from user input and displays them in a list."""
        await ctx.send(f"Arguments: {', '.join(args)}")

    @commands.command(name="format_timestamp", help="Formats a timestamp into a user-friendly string.")
    async def format_timestamp(self, ctx: commands.Context, timestamp: int):
        """Formats a timestamp into a user-friendly string."""
        try:
            formatted_timestamp = discord.utils.format_dt(discord.utils.snowflake_time(timestamp), "F")
            await ctx.send(f"Formatted Timestamp: {formatted_timestamp}")
        except Exception as e:
            await ctx.send(f"Error: {e}")

    @commands.command(name="send_error", help="Sends a formatted error message.")
    async def send_error(self, ctx: commands.Context, error_message: str):
        """Sends a formatted error message to the user."""
        embed = discord.Embed(title="Error", description=error_message, color=discord.Color.red())
        await ctx.send(embed=embed)

    @commands.command(name="log_event", help="Logs an event to the console.")
    async def log_event(self, ctx: commands.Context, message: str):
        """Logs a message to the console."""
        logging.info(f"Event: {message}")
        await ctx.send(f"Event logged: {message}")

def setup(bot: commands.Bot):
    bot.add_cog(UtilityCog(bot))