import asyncio
import sys
import subprocess
import random

import discord
from discord.ext import commands

# `Wrapper` and `Translator`. See in "Core/Wrapper.py"
from Core.Wrapper import Wrapper, Translate

# Main settings
from Core.Settings import BOT_TOKEN
from Core.Settings import BOT_LOCALE
from Core.Settings import BOT_COMMAND_PREFIX
from Core.Settings import BOT_CASE_SENSETIVE

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
			status=discord.Status.invisible,
			activity=game,
		)
		await asyncio.sleep(timer)


@bot.event
async def on_message(ctx):
	# simple text wrapper
	patterns = _("message-patterns")
	if ctx.author != bot.user:
		if ctx.content in patterns:
			message = patterns[ctx.content.lower()]
			if isinstance(message, list):
				await ctx.channel.send(random.choice(message))
			if isinstance(message, str):
				await ctx.channel.send(message)

	await bot.process_commands(ctx)

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