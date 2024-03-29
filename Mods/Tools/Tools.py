"""
TODO:
* Add check user id in `restart` and `reload_module`
* Add `set/add/delete status, module`
"""

import os, sys, subprocess, re

import discord
from discord.ext import commands
from discord.permissions import Permissions
from discord.ext.commands import ExtensionNotFound
from discord.ext.commands import ExtensionNotLoaded
from discord.ext.commands import NoEntryPointError
from discord.ext.commands import ExtensionFailed

from Core.Settings import COLORS
from Core.Settings import ADMIN_ROLES
from Core.Settings import BOT_PROFILE_PICTURE
from Core.Settings import DOCS_LINK
from Core.Settings import BOT_RESTART_CLEAR_CONSOLE
from Core.Settings import OS_CLR
from Core.Settings import MODS

from Core.Translate import Translate
from Core.SQL import get_guilds, update


translate = Translate("Mods/Tools/Locales")
tr = translate.get
alias = translate.getalias


class Tools(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases=alias("set-prefix"), pass_context=True)
	async def set_prefix(self, ctx, prefix):
		if Permissions.administrator:
			regex = re.compile(r"[@_!#$%^&*()<>?/\|}{~:]")
			# If prefix is a word then add space
			if not regex.search(prefix):
				prefix += " "

			guild = str(ctx.message.guild.id)
			update(guild, prefix=prefix)
			await ctx.send(tr("Done. Prefix is - {prefix}", ctx=ctx, prefix=prefix))

	@commands.command(aliases=alias("set-locale"), pass_context=True)
	async def set_locale(self, ctx, locale):
		if Permissions.administrator:
			regex = re.compile(r"[a-z]{2}-[A-Z]{2}")
			if regex.search(locale):
				guild = str(ctx.message.guild.id)
				update(guild, lc=locale)
				await ctx.send("Done. Locale is - {locale}", ctx=ctx, locale=locale)
			else:
				await ctx.send("Sosi")

	@commands.command(aliases=alias("restart"), pass_context=True)
	@commands.is_owner()
	async def restart(self, ctx):
		embed = discord.Embed(
			title=tr("Rebooting", ctx=ctx, emoji="gear"),
			color=COLORS.get("orange", 0x99ccff),
		)
		await ctx.send(embed=embed)

		if BOT_RESTART_CLEAR_CONSOLE:
			subprocess.call(OS_CLR[sys.platform], shell=True)
		subprocess.call([sys.executable, "Bot.py"])

	@restart.error
	async def restart_error(self, ctx, error):
		if isinstance(error, commands.NotOwner):
			await ctx.send(tr("Not a owner", ctx=ctx, emoji="alien"))

	@commands.command(aliases=alias("reload-module"), pass_context=True)
	@commands.is_owner()
	async def reload_module(self, ctx, *mods):
		# `prefix <reload_module> *`
		# `prefix <reload_module> ModName1 ModName2 ... ModNameX`
		if "*" in mods:
			mods = (i.split(".")[-1] for i in MODS)

		for mod in mods:
			try:
				self.bot.reload_extension("Mods.{mod}.{mod}".format(mod=mod))
				await ctx.send(tr("Module was rebooted - `{module}`", ctx=ctx, emoji="wrench", module=mod))

			except ExtensionNotFound:
				await ctx.send(tr("Module doesn't exist - `{module}`", ctx=ctx, emoji="warning", module=mod))

			except Exception as err:
				await ctx.send(tr("Failed to reboot module - `{module}`", ctx=ctx, emoji="fire", module=mod, error=err))

	@reload_module.error
	async def reload_module_error(self, ctx, error):
		if isinstance(error, commands.NotOwner):
			await ctx.send(tr("Not a owner", ctx=ctx))

		if isinstance(error, commands.BadArgument):
			await ctx.send("Hmmm")

	@commands.command(aliases=alias("info"), pass_context=True)
	async def info(self, ctx):
		embed = discord.Embed(
			title=tr("The best bot in the world", ctx=ctx, emoji="small_blue_diamond"),
			color=COLORS["blue"],
		)

		embed.set_image(
			url=BOT_PROFILE_PICTURE,
		)

		embed.add_field(
			name=tr("Author", ctx=ctx, emoji="small_blue_diamond"),
			value="useless_vevo#2169",
		)

		embed.add_field(
			name=tr("Commands", ctx=ctx, emoji="small_blue_diamond"),
			value=DOCS_LINK,
		)

		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(Tools(bot))