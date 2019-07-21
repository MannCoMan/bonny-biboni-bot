import asyncio
import sys
import subprocess
import random
import datetime
import time

import discord
from discord.ext import commands

# `Wrapper` and `Translator`. See in "Core/Wrapper.py"
from Core.Wrapper import Wrapper, Translate

# Main settings
from Core.Settings import BOT_TOKEN
from Core.Settings import BOT_LOCALE
from Core.Settings import BOT_COMMAND_PREFIX
from Core.Settings import BOT_CASE_SENSETIVE

# Logs
from Core.Settings import BOT_ENABLE_LOGS
from Core.Settings import BOT_LOG_CHANNELS

# Extensions. See in "Mods"
from Core.Settings import MODS
from Core.Settings import DEVMODE_MODS

# Status presence and "Dev Mode"
from Core.Settings import BOT_GAME_STATUSES
from Core.Settings import BOT_STATUS_TIMER
from Core.Settings import BOT_GAME_STATUSES
from Core.Settings import BOT_REMOVED_COMMANDS
from Core.Settings import BOT_ENABLE_DEV_MODE
from Core.Settings import BOT_DEV_MODE_STATUS


_ = Translate("Locales").get

bot = commands.Bot(
	command_prefix=BOT_COMMAND_PREFIX,
	case_insensitive=BOT_CASE_SENSETIVE,
	description="Debil",
)
bot.remove_command(BOT_REMOVED_COMMANDS)


async def bot_tasks():
	if BOT_ENABLE_DEV_MODE:
		status = BOT_DEV_MODE_STATUS
		timer = BOT_STATUS_TIMER
	else:
		status = BOT_GAME_STATUSES
		timer = 1

	if len(status) == 1:
		game = discord.Game(name=status)
	else:
		game = discord.Game(name=random.choice(status))

	while True:
		await bot.change_presence(
			status=discord.Status.online,
			activity=game,
		)
		await asyncio.sleep(timer)


@bot.event
async def on_message(ctx):
	patterns = _("message-patterns")

	if ctx.author != bot.user:
		if ctx.content in patterns:
			message = patterns[ctx.content.lower()]
			if isinstance(message, list):
				await ctx.channel.send(random.choice(message))
			if isinstance(message, str):
				await ctx.channel.send(message)

	await bot.process_commands(ctx)


@bot.event
async def on_command(ctx):
	channel = bot.get_channel(BOT_LOG_CHANNELS["on_command"])
	embed = discord.Embed(
		title="Author",
		description=f"{ctx.message.author} from {ctx.message.guild}",
		timestamp=datetime.datetime.fromtimestamp(time.time())
	)
	embed.add_field(
		name="Command",
		value=ctx.message.content,
		inline=True
	)
	await channel.send(embed=embed)

@bot.event
async def on_command_error(ctx, e):
	channel = bot.get_channel(BOT_LOG_CHANNELS["on_command_error"])
	embed = discord.Embed(
		title="Author",
		description=f"{ctx.message.author} from {ctx.message.guild}",
		timestamp=datetime.datetime.fromtimestamp(time.time())
	)

	if isinstance(e, commands.CommandOnCooldown):
		message = f":clock1: Please, wait, {ctx.message.author.mention}!"

	if isinstance(e, commands.UserInputError):
		message = f":warning: Invalid input in the '{ctx.command}!"

	if isinstance(e, commands.BadArgument):
		message = f":warning: Command '{ctx.command.content}' got bad argument!"

	if isinstance(e, commands.CommandNotFound):
		message = f":warning: Command `{ctx.message.content}` is not found!"

	if isinstance(e, UnboundLocalError):
		print(f"Hidden error: {e}")

	embed.add_field(
		name="Command",
		value=message,
		inline=True
	)
	await ctx.send(message)
	await channel.send(embed=embed)

@bot.listen()
async def on_ready():
	print(f"Bot login: {bot.user.name}\nBot id: {bot.user.id}\n")
	bot.loop.create_task(bot_tasks())


if __name__ == "__main__":
	for ext in MODS:
		try:
			bot.load_extension(ext)
			print(f"Mod was successfully loaded - '{ext}'")
		except Exception as e:
			print(f"Failed to load mod {ext}\n{type(e).__name__}: {e}")

	bot.run(BOT_TOKEN)