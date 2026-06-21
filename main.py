import discord
from deep_translator import GoogleTranslator
from better_profanity import profanity
from discord.ext import commands
import logging
from dotenv import load_dotenv
from collections import defaultdict
import asyncio
import time
import os

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

handle = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
profanity.load_censor_words()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):

    if message.content in ["مين انا", "مين انا ؟"]:
        if message.author.name == "its_sharif1":
            await message.channel.send("صانعي العظيم")
        else:
            await message.channel.send("واحد زربة")

    if message.author == bot.user:
        return

    is_owner = message.guild is not None and message.author == message.guild.owner

    if not is_owner:
        try:
            translated_text = await asyncio.to_thread(
                lambda: GoogleTranslator(source='auto', target='en').translate(message.content)
            )
            print(f"Original: {message.content}")
            print(f"Translated: {translated_text}")

            if profanity.contains_profanity(message.content) or profanity.contains_profanity(translated_text):
                await message.delete()
                await message.channel.send(f"{message.author.name} استخدم كلمات بذيئة")
                return

        except Exception as e:
            print(f"Translation error: {e}")

    await bot.process_commands(message)

@bot.command()
async def بنيامين_عباس(ctx):
    await ctx.send(file=discord.File("assets/benjamin_abbas.gif"))

bot.run(token, log_handler=handle, log_level=logging.DEBUG)
