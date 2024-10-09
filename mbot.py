import discord
import openai
import schedule
import time
import os

from discord.ext import commands
from threading import Thread
from datetime import datetime

# Initialize the Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Set your OpenAI API Key and Discord Bot Token
OPENAI_API_KEY = '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'
DISCORD_TOKEN = 'MTI5MzY4NTU0ODgxNjI3MzUyMA.G_aEli.Kd2S7nARjjqvexqoIuYcIfLUeSYUFscX6B8NWI'
CHANNEL_ID = 1293686245465260104  # Replace with your Discord channel ID

openai.api_key = OPENAI_API_KEY

# Function to generate a Yoda-style phrase using OpenAI API
def generate_yoda_phrase():
    prompt = "Give me a motivational message in Yoda's sentence structure."
    response = openai.Completion.create(
        model="gpt-4",
        prompt=prompt,
        max_tokens=60
    )
    return response['choices'][0]['text'].strip()

# Function to send a message to a Discord channel
async def send_message_to_discord(channel_id, text):
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(text)

# Function to handle scheduled message
def schedule_message(time_to_send):
    yoda_message = generate_yoda_phrase()
    
    # Schedule the message at the given time
    schedule.every().day.at(time_to_send).do(
        lambda: asyncio.run_coroutine_threadsafe(
            send_message_to_discord(CHANNEL_ID, f"Yoda says: {yoda_message}"), bot.loop
        )
    )

    while True:
        schedule.run_pending()
        time.sleep(1)

# Command to schedule a message
@bot.command(name='schedule')
async def schedule_command(ctx, time_to_send: str):
    """Schedule a Yoda message at the specified time. Example: !schedule 09:00"""
    try:
        # Validate time format
        datetime.strptime(time_to_send, "%H:%M")
        
        # Start a new thread for scheduling to avoid blocking
        t = Thread(target=schedule_message, args=(time_to_send,))
        t.start()

        await ctx.send(f"Message scheduled for {time_to_send} every day.")
    except ValueError:
        await ctx.send("Invalid time format. Please use HH:MM (24-hour format).")

# Bot ready event
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

if __name__ == '__main__':
    bot.run(DISCORD_TOKEN)
