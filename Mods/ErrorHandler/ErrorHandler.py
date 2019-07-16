import discord
from discord.ext import commands
from Core.Settings import *


class CommandErrorHandler(commands.Cog):
	def __init__(self, bot, **kwargs):
		self.bot = bot

	async def on_command_error(self, e, ctx):
		channel_id = ctx.get_channel(BOT_LOG_CHANNEL)

		if isinstance(e, commands.UserInputError):
			await ctx.send(
				ctx.get_channel(BOT_LOG_CHANNEL), 
				f"Invalid input in the '{ctx.command}. Message from {channel_id.mention}"
			)

		if isinstance(e, commands.BadArgument):
			await ctx.send(
				ctx.get_channel(BOT_LOG_CHANNEL), 
				f"Function '{ctx.command.content}' got bad argument. Message from {channel_id.mention}"
			)

		if isinstance(e, commands.CommandNotFound):
			await ctx.send(
				ctx.get_channel(BOT_LOG_CHANNEL),
				f"Command `{ctx.message.content}` is not found!. Message from {channel_id.mention}"
			)

	async def on_error(self, e, ctx):
		await ctx.send(
			ctx.get_channel(BOT_LOG_CHANNEL),
			f"Error: '{e}'"
		)

    # Below is an example of a Local Error Handler for our command do_repeat
	@commands.command(name='repeat', aliases=['mimic', 'copy'])
	async def do_repeat(self, ctx, *, inp: str):
		await ctx.send(inp)
		
	@do_repeat.error
	async def do_repeat_handler(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			if error.param.name == 'inp':
				await ctx.send("You forgot to give me input to repeat!")

def setup(bot, **kwargs):
	bot.add_cog(CommandErrorHandler(bot, **kwargs))