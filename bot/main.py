import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
# 1. Turn on the default intents
intents = discord.Intents.default()
# 2. Specifically turn ON the message content intent
intents.message_content = True

# 3. Add the 'intents' to your bot variable
bot = commands.Bot(command_prefix="!", intents=intents)
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

commands.bot = commands.Bot(command_prefix='!', intents=intents)

secret_role = "Gamer"

@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} - dont use that word!")

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {secret_role}")
    else:
        await ctx.send("Role doesn't exist")

@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has had the {secret_role} removed")
    else:
        await ctx.send("Role doesn't exist")

@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"You said {msg}")

@bot.command()
async def reply(ctx):
    await ctx.reply("This is a reply to your message!")

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="New Poll", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

@bot.command()
@commands.has_role(secret_role)
async def secret(ctx):
    await ctx.send("Welcome to the club!")

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to do that!")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
from keep_alive import keep_alive
# ... your other imports ...

keep_alive()  # This starts the web server
# ---------------------------------------------------------
# LOGGING SYSTEM
# ---------------------------------------------------------

# Replace this number with the ID of a private channel in your server
# Right-click a channel in Discord and click "Copy Channel ID"
LOG_CHANNEL_ID = 123456789012345678


@bot.event
async def on_message(message):
    # 1. Ignore the bot's own messages so it doesn't log itself
    if message.author.bot:
        return

    # 2. Log every single chat to the Render Console
    print(f"[CHAT] {message.guild.name} | #{message.channel.name} | {message.author}: {message.content}")

    # 3. CRITICAL: You must include this line at the end of on_message,
    # otherwise your other @bot.command() commands will stop working!
    await bot.process_commands(message)


@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return

    # Find the secret logging channel
    log_channel = bot.get_channel(LOG_CHANNEL_ID)

    if log_channel:
        # Create a nice looking embed for the deleted message
        embed = discord.Embed(
            title="🗑️ Message Deleted",
            description=f"A message from {message.author.mention} was deleted in {message.channel.mention}.",
            color=discord.Color.red()
        )
        # Add the actual text that was deleted
        embed.add_field(name="Deleted Content:", value=message.content or "*No text (might have been an image)*",
                        inline=False)

        # Send it to your private log channel
        await log_channel.send(embed=embed)


@bot.event
async def on_message_edit(before, after):
    # Don't log if a bot did it, or if the text didn't actually change (like if an embed loaded)
    if before.author.bot or before.content == after.content:
        return

    log_channel = bot.get_channel(LOG_CHANNEL_ID)

    if log_channel:
        embed = discord.Embed(
            title="✏️ Message Edited",
            description=f"{before.author.mention} edited a message in {before.channel.mention}.",
            color=discord.Color.orange()
        )
        embed.add_field(name="Before:", value=before.content or "*Empty*", inline=False)
        embed.add_field(name="After:", value=after.content or "*Empty*", inline=False)

        await log_channel.send(embed=embed)