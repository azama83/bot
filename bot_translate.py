import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from deep_translator import GoogleTranslator

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
FR_CHANNEL_ID = 1420386356647166052  # ID de ton salon #français
EN_CHANNEL_ID = 1420386460443480064  # ID de ton salon #english

# --- INTENTS ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- FONCTION DE TRADUCTION ---
def translate(text, source_lang, target_lang):
    try:
        return GoogleTranslator(source=source_lang, target=target_lang).translate(text)
    except Exception as e:
        print("Erreur traduction:", e)
        return text

# --- ÉVÉNEMENT MESSAGE ---
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Traduction français -> anglais
    if message.channel.id == FR_CHANNEL_ID:
        translated = translate(message.content, "fr", "en")
        en_channel = bot.get_channel(EN_CHANNEL_ID)
        if en_channel:
            await en_channel.send(f"**{message.author.display_name} (FR):** {translated}")

    # Traduction anglais -> français
    elif message.channel.id == EN_CHANNEL_ID:
        translated = translate(message.content, "en", "fr")
        fr_channel = bot.get_channel(FR_CHANNEL_ID)
        if fr_channel:
            await fr_channel.send(f"**{message.author.display_name} (EN):** {translated}")

    await bot.process_commands(message)

# --- LANCER LE BOT ---
bot.run(TOKEN)
