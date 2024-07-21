import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize Discord intents
intents = discord.Intents.default()
intents.members = True  # Enable member intents to retrieve user information
intents.message_content = True  # Enable message content intents to read message content

# Create bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# Load cogs
@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user.name} (ID: {bot.user.id})')

    # Load cogs for music, administration, and utilities
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')

# Run the bot
if __name__ == '__main__':
    # Get Discord bot token from environment variable
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        logging.error("DISCORD_TOKEN is not set in .env file")
        exit(1)

    # Start the bot
    bot.run(token)