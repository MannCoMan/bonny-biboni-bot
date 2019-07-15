import sys, subprocess

import discord
from discord.ext import commands

from Core.Settings import COLORS
from Core.Settings import ADMIN_ROLES
from Core.Settings import BOT_PROFILE_PICTURE
from Core.Settings import DOCS_LINK
from Core.Settings import BOT_RESTART_CLEAR_CONSOLE
from Core.Settings import OS_CLR


class Tools(commands.Cog):
	def __init__(self, bot, **kwargs):
		self.bot = bot

	@commands.command(aliases=["рестарт", "ресет"], pass_context=True)
	@commands.has_any_role(*ADMIN_ROLES)
	# @commands.has_permissions(administrator=True, manage_messages=True, manage_roles=True)
	async def restart(self, ctx):
		embed = discord.Embed(
			title="ｒｅｓｔａｒｔ　憶ュギ",
			color=COLORS.get("orange", 0x99ccff),
		)
		await ctx.send(embed=embed)

		if BOT_RESTART_CLEAR_CONSOLE:
			subprocess.call(OS_CLR[sys.platform], shell=True)
		subprocess.call([sys.executable, "Bot.py"])

	@commands.command(aliases=["инфо", "информация", "инфа"], pass_context=True)
	async def info(self, ctx):
		try:
		    embed = discord.Embed(
				title="Лучший бот во всём мире",
				description="Не ебу, зачем он создан",
				color=COLORS["blue"],
			)

		    embed.set_image(
				url=BOT_PROFILE_PICTURE,
			)

		    embed.add_field(
				name="Автор: ",
				value="Useless VEVO#2169",
			)

		    embed.add_field(
				name="Команды: ",
				value=DOCS_LINK,
			)

		    await ctx.send(embed=embed)
		except Exception as e:
			raise Exception(e)


def setup(bot, **kwargs):
	bot.add_cog(Tools(bot, **kwargs))