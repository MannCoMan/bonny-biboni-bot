import discord
from discord.ext import commands


class ASCII:
	def __init__(self, bot):
		self.bot = bot

	@commands.group(aliases=["кот", "кiт"], pass_context=True)
	async def catface(self, ctx, *msg):
		if ctx.invoked_subcommand is None:
			msg = "%s - гей" % ctx.message.author.name
		else:
			msg = " ".join(msg)

		await self.bot.say("""\t∧∧\n(　･ω･) %s
		""" % msg)

	@commands.command(aliases=["кот-спит", "спящий"], pass_context=True)
	async def sleepycat(self, ctx, *msg):
		if ctx.invoked_subcommand is None:
			msg = "%s - гей" % ctx.message.author.name
		else:
			msg = " ".join(msg)

		await self.bot.say("""
			
			zzz 
			　＜⌒／ヽ-､＿
			／＜/＿＿＿＿／
			￣￣￣￣￣￣￣

			　　　∧∧　 
			　　 (　･ω･) %s
			　 ＿|　⊃／(＿ 
			／　└-(＿＿＿／ 
			￣￣￣￣￣￣￣ 

			zzz 
			　＜⌒／ヽ-､＿
			／＜/＿＿＿＿／
			￣￣￣￣￣￣￣
			""" % msg)

	@commands.command(aliases=["кот-танцор", "танцульки"], pass_context=True)
	async def dancingcat(self, ctx, *msg):
		if ctx.invoked_subcommand is None:
			msg = "%s - гей" % ctx.message.author.name
		else:
			msg = " ".join(msg)

		await self.bot.say("""
			⊂_ヽ 
			　 ＼＼ Λ＿Λ 
			　　 ＼( 'ㅅ' ) 
			　　　 >　⌒ヽ 
			　　　/ 　 へ＼ 
			　　 /　　/　＼＼ 
			　　 ﾚ　ノ　　 ヽ_つ 
			　　/　/ %s
			　 /　/| 
			　(　(ヽ 
			　|　|、＼ 
			　| 丿 ＼ ⌒) 
			　| |　　) / 
			`ノ )　　Lﾉ
			""" % msg)


def setup(bot):
	bot.add_cog(ASCII(bot))