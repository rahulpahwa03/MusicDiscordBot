import discord
from discord.ext import commands
from discord.utils import get
import os
import youtube_dl

TOKEN = 'add your own discord token here'
bot = commands.Bot(command_prefix='!')



# bot online cmd
@bot.event
async def on_ready():
    print("bot online")



# join vc command
@bot.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
   
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")
    
    # sending message in discord
    title = f"**JOINED CHANNEL {channel}**"
    description = f'Joined channel for beautiful streaming {ctx.author.mention}'

    embed = discord.Embed(title = title , discription= description, color= discord.Colour.green())
    embed.add_field(name = 'Streaming melodious songs' ,value= ctx.author.mention, inline=True)


    await ctx.send(embed=embed)




# Leave vc command
@bot.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
     channel = ctx.message.author.voice.channel
     voice = get(bot.voice_clients, guild=ctx.guild)

     if voice and voice.is_connected():
         await voice.disconnect()
         print(f"The bot has left the channel:{channel}")

         # sending message in discord
         title = f"**LEFT CHANNEL {channel}**"
         description = f'Joined channel for beautiful streaming {ctx.author.mention}'

         embed = discord.Embed(title = title , discription= description, color= discord.Colour.green())
         embed.add_field(name = 'You will miss my songs' ,value= ctx.author.mention, inline=True)


         await ctx.send(embed=embed)

         
     else:
         print("bot was told to leave the channel,but not was in any")
        
         # sending message in discord
         title = f"**I NEVER JOINED CHANNEL {channel}**"
         description = f'Joined channel for beautiful streaming {ctx.author.mention}'

         msg = discord.Embed(title = title , discription= description, color= discord.Colour.green())
         msg.add_field(name = 'YOU ARE NOOB ' ,value= ctx.author.mention, inline=True)


         await ctx.send(embed=msg)



# play music with url command
@bot.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):
    song_there = os.path.isfile('song.mp3')
    try:
        if song_there:
            os.remove('song.mp3')
            print("removed old song")
    except PermissionError:
        print("tried to remove old song but its currently playing.")
        await ctx.send("ERROR: song playing")
        return

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song done!"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("playing\n")



# pause command
@bot.command(pass_context=True, aliases=['pau', 'pus'])
async def pause(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music paused!")

        voice.pause()

        await ctx.send(f"Paused! {ctx.author.mention}")

    else:
        print("music not playing, failed pause!")
        await ctx.send("**NO MUSIC IS PLAYING**")




# resume command
@bot.command(pass_context=True, aliases=['re', 'res'])
async def resume(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Music resumed!")

        voice.resume()

        await ctx.send(f"Resumed! {ctx.author.mention}")

    else:
        print("music is not paused")
        await ctx.send("**MUSIC IS NOT PAUSED**")




# stop command
@bot.command(pass_context=True, aliases=['s', 'st'])
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music Stoped!")

        voice.stop()

        await ctx.send(f"Stoped playing! {ctx.author.mention}")

    else:
        print("music is not playing")
        await ctx.send("**MUSIC IS NOT PLAYING**")




bot.run(TOKEN)