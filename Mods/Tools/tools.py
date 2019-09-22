"""
TODO:
* Add check user id in `restart` and `reload_module`
* Add `set/add/delete status, module`
"""

import os, sys, subprocess, re

import discord
from discord.ext import commands
from discord.permissions import Permissions
from discord.audit_logs import AuditLogEntry
from discord.ext.commands import ExtensionNotFound
from discord.ext.commands import ExtensionNotLoaded
from discord.ext.commands import NoEntryPointError
from discord.ext.commands import ExtensionFailed

from .constants import ToolsConst
from Core.tools import get_color
from Core.translate import Translate
from Core.sql import update


translate = Translate("Mods/Tools/Locales")
tr = translate.get
alias = translate.getalias


class Tools(commands.Cog):
	Const = ToolsConst()
	
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases=alias("set-prefix"), pass_context=True)
	async def set_prefix(self, ctx, prefix):
		if Permissions.administrator:
			regex = re.compile(r"[@_!#$%^&*()<>?/\|}{~:]")
			# if prefix is a word then add space
			if not regex.search(prefix):
				prefix += " "

			await ctx.send(tr("Done. Prefix is - {prefix}", ctx=ctx, prefix=prefix))
			guild = ctx.message.guild.id
			update(guild, prefix=prefix)

	@commands.command(aliases=alias("set-locale"), pass_context=True)
	async def set_locale(self, ctx, locale):
		if Permissions.administrator:
			regex = re.compile(r"[a-z]{2}-[A-Z]{2}")
			# locale format - lc-LC
			# change it to emoji listener
			if regex.search(locale):
				guild = ctx.message.guild.id
				update(guild, lc=locale)
				await ctx.send("Done. Locale is - {locale}", ctx=ctx, locale=locale)
			await ctx.send("Sosi")

	@commands.command(aliases=alias("purge-message"), pass_context=True)
	async def purge_message(self, ctx, value):
		if Permissions.administrator:
			# AuditLogEntry.category
			pass


	@commands.command(aliases=alias("restart"), pass_context=True)
	@commands.is_owner()
	async def restart(self, ctx):
		embed = discord.Embed(
			title=tr("Rebooting", ctx=ctx, emoji="gear"),
			color=get_color("orange"),
		)
		await ctx.send(embed=embed)

		if self.Const.BOT_RESTART_CLEAR_CONSOLE:
			subprocess.call(self.Const.OS_CLR[sys.platform], shell=True)
		subprocess.call([sys.executable, "bot.py"])

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
			mods = list(".".join(i.split(".")[1:]) for i in self.Const.MODS)

		for mod in mods:
			try:
				self.bot.reload_extension("Mods.{}".format(mod))
				await ctx.send(tr("Module was rebooted - `{module}`", ctx=ctx, emoji="wrench", module=mod))

			except ExtensionNotFound as err:
				await ctx.send(tr("Module doesn't exist - `{module}`", ctx=ctx, emoji="warning", module=mod))
				print(err)

			except Exception as err:
				await ctx.send(tr("Failed to reboot module - `{module}`", ctx=ctx, emoji="fire", module=mod, error=err))
				print(err)

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
			color=get_color("blue"),
		)

		embed.set_image(
			url=self.Const.BOT_PROFILE_PICTURE,
		)

		embed.add_field(
			name=tr("Author", ctx=ctx, emoji="small_blue_diamond"),
			value="useless_vevo#2169",
		)

		embed.add_field(
			name=tr("Commands", ctx=ctx, emoji="small_blue_diamond"),
			value=self.Const.BOT_DOCS_LINK,
		)

		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(Tools(bot))