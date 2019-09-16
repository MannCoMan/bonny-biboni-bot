import asyncio
import sys
import subprocess
import random
import datetime
import time

import discord
from discord.ext import commands

from Core.Wrapper import Wrapper
from Core.Translate import Translate
from Core.SQL import get_guilds
from Core.SQL import update
from Core.SQL import insert

# Main settings
from Core.Settings import BOT_TOKEN
from Core.Settings import BOT_DEFAULT_PREFIX
from Core.Settings import BOT_CASE_SENSETIVE

# Logs
from Core.Settings import BOT_ENABLE_LOGS
from Core.Settings import BOT_LOG_CHANNELS

# Extensions. See in "Mods"
from Core.Settings import MODS
from Core.Settings import DEVMODE_MODS

# Status presence and "Dev Mode"
from Core.Settings import BOT_STATUS_TIMER
from Core.Settings import BOT_GAME_STATUSES
from Core.Settings import BOT_DEV_STATUSES
from Core.Settings import BOT_REMOVED_COMMANDS
from Core.Settings import BOT_ENABLE_DEV_MODE


tr = Translate("Locales").get


async def get_prefix(bot, ctx):
	guild = str(ctx.guild.id)
	guild, _, prefix = get_guilds(gid=guild)[0]
	return [prefix, BOT_DEFAULT_PREFIX]


bot = commands.Bot(
	command_prefix=get_prefix,
	case_insensitive=BOT_CASE_SENSETIVE,
	description="Debil",
)
bot.remove_command(BOT_REMOVED_COMMANDS)


async def bot_tasks():
	if BOT_ENABLE_DEV_MODE:
		status = BOT_DEV_STATUSES
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
async def on_guild_join(ctx):
	pass


@bot.event
async def on_command(ctx):
	channel = bot.get_channel(BOT_LOG_CHANNELS["on_command"])

	embed = discord.Embed(
		title=tr("Author", ctx=ctx),
		description="{} - {}".format(ctx.message.author, ctx.message.guild),
		timestamp=datetime.datetime.fromtimestamp(time.time())
	)

	embed.add_field(
		name=tr("Command", ctx=ctx),
		value=ctx.message.content,
		inline=True
	)

	await channel.send(embed=embed)


@bot.event
async def on_command_error(ctx, e):
	channel = bot.get_channel(BOT_LOG_CHANNELS["on_command_error"])
	
	embed = discord.Embed(
		title=tr("Author", ctx=ctx),
		description="{} - {}".format(ctx.message.author, ctx.message.guild),
		timestamp=datetime.datetime.fromtimestamp(time.time())
	)

	if isinstance(e, commands.CommandOnCooldown):
		message = tr("Please, wait", ctx=ctx, emoji="clock1", member=ctx.message.author.mention)
		embed.add_field(name=tr("Command", ctx=ctx), value=message, inline=True)
		await channel.send(embed=embed)

	if isinstance(e, commands.UserInputError):
		message = tr("Invalid input", ctx=ctx, emoji="warning", err=ctx.command)
		embed.add_field(name=tr("Command", ctx=ctx), value=message, inline=True)
		await channel.send(embed=embed)

	if isinstance(e, commands.BadArgument):
		message = tr("Bad command argument in", emoji="warning", err=ctx.command.content)
		embed.add_field(name=tr("Command", ctx=ctx), value=message, inline=True)
		await channel.send(embed=embed)

	if isinstance(e, commands.CommandNotFound):
		message = tr("Command not found", ctx=ctx, emoji="warning", err=ctx.message.content)
		embed.add_field(name=tr("Command", ctx=ctx), value=message, inline=True)
		await channel.send(embed=embed)

	if isinstance(e, UnboundLocalError):
		message = "Hidden error: {}".format(e)
		embed.add_field(name=tr("Command", ctx=ctx), value=message, inline=True)
		await channel.send(embed=embed)


@bot.listen()
async def on_ready():
	print("Bot login: {}\nBot id: {}\n".format(
		bot.user.name,
		bot.user.id
	))
	bot.loop.create_task(bot_tasks())


if __name__ == "__main__":
	for ext in MODS:
		try:
			bot.load_extension(ext)
			print("Mod was successfully loaded - '{}'".format(ext))
		except discord.ext.commands.errors.ExtensionNotFound as err:
			print("Failed to load mod {}\n{}: {}".format(ext, type(ext).__name__, err))

	bot.run(BOT_TOKEN)