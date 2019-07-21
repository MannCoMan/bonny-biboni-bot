import os, sys, subprocess

import discord
from discord.ext import commands
from discord.ext.commands import ExtensionNotFound
from discord.ext.commands import ExtensionNotLoaded
from discord.ext.commands import NoEntryPointError
from discord.ext.commands import ExtensionFailed

from Core.Settings import COLORS
from Core.Settings import ADMIN_ROLES
from Core.Settings import BOT_LOCALE
from Core.Settings import BOT_PROFILE_PICTURE
from Core.Settings import DOCS_LINK
from Core.Settings import BOT_RESTART_CLEAR_CONSOLE
from Core.Settings import OS_CLR
from Core.Settings import MODS

from Core.Wrapper import Translate


_ = Translate("Mods", "Tools", "Locales").get

class Tools(commands.Cog):
	def __init__(self, bot, **kwargs):
		self.bot = bot

	@commands.command(aliases=_("aliases", "restart"), pass_context=True)
	@commands.is_owner()
	# @commands.has_permissions(administrator=True, manage_messages=True, manage_roles=True)
	async def restart(self, ctx):
		embed = discord.Embed(
			title=_("restart-header"),
			color=COLORS.get("orange", 0x99ccff),
		)
		await ctx.send(embed=embed)

		if BOT_RESTART_CLEAR_CONSOLE:
			subprocess.call(OS_CLR[sys.platform], shell=True)
		subprocess.call([sys.executable, "Bot.py"])

	@restart.error
	async def restart_error(self, ctx, error):
		if isinstance(error, commands.NotOwner):
			await ctx.send(_("not-owner"))

	@commands.command(aliases=_("aliases", "reload-module"), pass_context=True)
	@commands.is_owner()
	async def reload_module(self, ctx, *mods):
		# `prefix <reload_module> *`
		# `prefix <reload_module> ModName1 ModName2 ... ModNameX`
		if "*" in mods:
			mods = (i.split(".")[-1] for i in MODS)

		for mod in mods:
			try:
				self.bot.reload_extension(f"Mods.{mod}.{mod}")
				await ctx.send(_("reload-module-done").format(mod=mod))
			except ExtensionNotFound:
				await ctx.send(_("reload-module-doesnt-exist").format(mod=mod))
			except Exception as e:
				await ctx.send(_("reload-module-failed").format(mod=mod))
				print(f"Failed to load mod {mod}\n{type(e).__name__}: {e}")

	@reload_module.error
	async def reload_module_error(self, ctx, error):
		if isinstance(error, commands.NotOwner):
			await ctx.send(_("not-owner"))
		if isinstance(error, commands.BadArgument):
			await ctx.send("Hmmm")

	@commands.command(aliases=_("aliases", "info"), pass_context=True)
	async def info(self, ctx):
		try:
		    embed = discord.Embed(
				title=_("info-descr-header"),
				description=_("info-descr-text"),
				color=COLORS["blue"],
			)

		    embed.set_image(
				url=BOT_PROFILE_PICTURE,
			)

		    embed.add_field(
				name=_("info-author-header"),
				value=_("info-author-text"),
			)

		    embed.add_field(
				name=_("info-commands-header"),
				value=DOCS_LINK,
			)

		    await ctx.send(embed=embed)
		except Exception as e:
			raise Exception(e)
			

def setup(bot, **kwargs):
	bot.add_cog(Tools(bot, **kwargs))