import discord
import youtube_dl
from discord.ext import commands
import os
from webserver import keep_alive

TOKEN = os.environ['TOKEN']
my_secret = os.environ['TOKEN']
bot_prefix = '.'

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix=bot_prefix, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

@bot.command()
async def play(ctx, url):
    voice_channel = ctx.author.voice.channel

    if voice_channel is None:
        await ctx.send("You are not in a voice channel.")
        return

    voice_channel = await voice_channel.connect()

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        voice_channel.play(discord.FFmpegPCMAudio(url2))

    await ctx.send(f"Now playing: {url}")

@bot.command()
async def stop(ctx):
    voice_channel = ctx.voice_client

    if voice_channel.is_playing():
        voice_channel.stop()
        await ctx.send("Playback stopped.")
    else:
        await ctx.send("No audio is currently playing.")

keep_alive()
bot.run(TOKEN)
