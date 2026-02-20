#importing section
import discord
import nacl
import random
import os
import ffmpeg
from discord.ext import commands

#Variable Data Value << Modify setting here
TOKEN = "Your Token Here"     #Bot Token
VoiceChannel = 12345678910 #Put a automatic Voice Channel
MusicLibrary = "path/To/your/music.mp3" #Path to Song
MessageReply = ["I'm Here...","Yes?~","Hmm?~","I'm Columbina Hyposelenia"] # Custom Mentioned message

#Variable Data Process 
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.presences = True
intents.typing = True
bot = commands.Bot(command_prefix= "c!", intents=intents) #<< Modify Prefix inside String

#Function area
def LoopPlay(vc, MusicLibrary): #Looping Song
    if vc and vc.is_connected():
        vc.play(discord.FFmpegPCMAudio(MusicLibrary), after=lambda e: LoopPlay(vc,MusicLibrary))

#Bot Event Process
@bot.event
async def on_ready(): # Bot Activate
    print(f"Succesfully Logged in As {bot.user} (ID : {bot.user.id})")
    message = await bot.fetch_channel(VoiceChannel)
    await message.send("*(A soft fluttering of wings)...*")
    await message.send("I am here. It's so loud in this world, isn't it? Let's be quiet together.")

    #Presence
    activity = discord.Activity(
        type = discord.ActivityType.listening,
        name = "Drifting Through Your Dream..."
        )
    await bot.change_presence(activity=activity)

    #Auto Voice Connect
    channel = await bot.fetch_channel(VoiceChannel)
    vc = await channel.connect()
    LoopPlay(vc, MusicLibrary)

@bot.event #Mention reply message system
async def on_message(message):
    if message.author == bot.user:
        return
    elif bot.user.mentioned_in(message):
        await message.channel.send(random.choice(MessageReply))
    
    await bot.process_commands(message)

#Command bot
@bot.command()
async def joinme(ctx): #join command
    if ctx.voice_client: #if bot is already in voice
        await ctx.send("I'm Already Here...")
        await ctx.send("You're not naughty enough to call me twice, are you?")
        await ctx.send("Hehe~")
    
    elif ctx.author.voice: #if user is inside a voice
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send("I'm Here~")
        await ctx.send("I'll start humming... The room feels calm...")
        ctx.voice_client.play(discord.FFmpegPCMAudio(MusicLibrary), after=lambda e: LoopPlay(ctx.voice_client,MusicLibrary))

    else: #if user not in voice or bot is not in voice
        await ctx.send("i cant see where you at exactly...")
        await ctx.send("I'll wait for you to call me again soon...")

@bot.command()
async def leaveme(ctx): #leave command
    if ctx.voice_client:
        ctx.voice_client.stop() #Stop the song
        await ctx.voice_client.disconnect() # Disconnect
        await ctx.send("i have left my place...")
        await ctx.send("let's meet and talk again later soon... Traveler")

    else:
        await ctx.send("I'm currently not in my place right now...")
        await ctx.send("I can't leave my place twice...")


if __name__ == "__main__":
    bot.run(TOKEN) #run the bot 