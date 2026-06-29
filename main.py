import discord
from deep_translator import GoogleTranslator
from better_profanity import profanity
from discord.ext import commands
import logging
from dotenv import load_dotenv
import asyncio
import os
import re

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

handle = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

profanity.load_censor_words()
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F300-\U0001FAFF"
    "\U00002600-\U000027BF"
    "\U0001F1E6-\U0001F1FF"
    "\U00002700-\U000027BF"
    "]+",
    flags=re.UNICODE,
)

def strip_emoji(text: str) -> str:
    return EMOJI_PATTERN.sub("", text).strip()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content in ["مين انا", "مين انا ؟"]:
        if message.author.name == "its_sharif1":
            await message.channel.send("صانعي العظيم")
        else:
            await message.channel.send(f"واحد زربة {message.author.mention}")
        await bot.process_commands(message)
        return

    if message.author.name not in ["its_sharif1", "ahmedhaddad04"] :
        try:
            content_no_emoji = strip_emoji(message.content)

            if content_no_emoji:
                translated_text = await asyncio.to_thread(
                    lambda: GoogleTranslator(source='auto', target='en').translate(content_no_emoji)
                )
                print(f"Original: {content_no_emoji}")
                print(f"Translated: {translated_text}")

                if translated_text and (
                    profanity.contains_profanity(content_no_emoji)
                    or profanity.contains_profanity(translated_text)
                ):
                    await message.delete()
                    await message.channel.send(f"{message.author.mention} استخدم كلمات بذيئة")
                    return
        except Exception as e:
            print(f"Translation error: {e}")

    await bot.process_commands(message)

@bot.command(name="بنيامين_عباس")
async def benjamin_abbas(ctx):
    try:
        await ctx.send(file=discord.File("assets/benjamin_abbas.gif"))
    except FileNotFoundError:
        await ctx.send("الملف غير موجود في مجلد assets!")

@bot.command(name="هجوم")
async def attack(ctx):
    mentions_list = []
    
    for member in ctx.guild.members:
        if not member.bot: 
            mentions_list.append(f"{member.mention} يا زنجي")
    
    chunk_size = 30
    for i in range(0, len(mentions_list), chunk_size):
        chunk = mentions_list[i:i + chunk_size]
        message_to_send = "\n".join(chunk) 
        await ctx.send(message_to_send)

@bot.command(name="سلم_على")
async def send_to_user(ctx, member: discord.Member):
    allowed_users = ["its_sharif1", "kenji_sa1", "ahmedhaddad04"]
    if ctx.author.name in allowed_users: 
        try:
            for i in range(20):
                await member.send(f"يا {member.mention} يا زنجي")
                await asyncio.sleep(0.1)
            await ctx.send(f"سلمت على {member.mention}!")
        except discord.Forbidden:
            await ctx.send(f"بقدرش ارسل لـ {member.mention}")
    else:
        await ctx.send(f"امشي لك معاكش صلاحية يا {ctx.author.mention} ( ابلع )")

@bot.command(name="نادي_على")
async def idk(ctx, member: discord.Member):
    allowed_users = ["its_sharif1", "kenji_sa1", "ahmedhaddad04"]
    if ctx.author.name in allowed_users:
        try:
            for i in range(20):
                await ctx.send(f"يا {member.mention} يا زنجي")
                await asyncio.sleep(0.1)
        except Exception as e:
            print(f"حدث خطأ: {e}")
    else:
        await ctx.send(f"امشي لك معاكش صلاحية يا {ctx.author.mention} ( ابلع )")
    
bot.run(token, log_handler=handle, log_level=logging.DEBUG)
