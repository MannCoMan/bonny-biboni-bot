import random
import discord
from discord.ext import commands

from Core.Wrapper import Wrapper, Translate
from Core.Settings import *


_ = Translate(BOT_LOCALE).get

class Games:
	def __init__(self, bot):
		self.rooms = {}
		self.users = {}
		self.bot = bot

	# Krutis', manya

	@commands.command(name='roll', aliases=['очко'], pass_context=True)
	async def ochko(self, ctx):
		rand = random.choice(_('roll'))
		await ctx.send(f"{ctx.message.author.mention}, {_('', 'ur')} - {rand}")

	# Roll the dice

	@commands.command(aliases=["кубики"], pass_context=True)
	async def rtd(self, ctx, args=99):
		rand = random.randrange(1, int(args))
		await ctx.send(f"{ctx.message.author.mention}, {_('messages', 'result')}: {rand}")

	# Russian roulette

	@commands.group(aliases=["рулетка"], pass_context=True)
	async def rr(self, ctx):
		self.embed = discord.Embed()
		if ctx.invoked_subcommand is None:
			await self.bot.say(":no_entry: Для создания комнаты набери: \"рулетка/rr <название комнаты>\"")

	@rr.command(pass_context=True)
	async def new(self, ctx, room:str):
		if room in self.rooms:
			await self.bot.say("Комната %s уже существует" % room)
		else:
			self.rooms[room] = {'name':'', 'owner':'', 'players':[], 'limit':6, 'bullets':6, 'shot':0}
			self.rooms[room]['name'] = room
			self.rooms[room]['owner'] = ctx.message.author.name
			self.rooms[room]['players'].append(ctx.message.author.name)
			self.rooms[room]['shot'] = random.randrange(0, self.rooms[room]['bullets'])
			self.users[ctx.message.author.name] = room

			embed = discord.Embed(title=_('main', 'help-header', case=3), color=COLORS["drk_magenta"])
			embed.title = _('messages', 'room-created', case=3).format(room)
			# embed.color = self.config.gv('colors', 'drk_blue', conv=int)
			embed.add_field(name="Owner", value=self.rooms[room]['owner'])
			embed.add_field(name="Limit", value=self.rooms[room]['limit'])
			embed.add_field(name="Players", value='\n'.join(self.rooms[room]['players']))
			await self.bot.say(embed=embed)

	@rr.command(aliases=["войти", "вступить"], pass_context=True)
	async def join(self, ctx, room:str):
		self.users[ctx.message.author.name] = room

		if len(self.rooms[room]['players']) == self.rooms[room]['limit']:
			message = '{0}, {1}'.format(ctx.message.author.mention, _('errors', 'room-is-full'))
			await self.bot.say(message)
		else:
			pass

		if ctx.message.author.name in self.rooms[room]['players']:
			message = '{0}, {1}'.format(ctx.message.author.mention, _('errors', 'user-in-room'))
			await self.bot.say(message)
		else:
			self.rooms[room]['players'].append(ctx.message.author.name)
			message = '{0}, {1} {2}'.format(ctx.message.author.mention, _('messages', 'user-was-added'), room)
			await self.bot.say(message)

	@rr.command(aliases=["погнали"], pass_context=True)
	async def roll(self, ctx):
		room = self.users[ctx.message.author.name]
		shot_tmp = random.randrange(1, self.rooms[room]['bullets'])
		users_tmp = self.rooms[room]['players']
		# run = False
		# queue = {}
		# for i,j in enumerate(users_tmp): queue[j] = i

		if shot_tmp == self.rooms[room]['shot']:
			self.rooms[room]['shot'] = random.randrange(0, self.rooms[room]['bullets'])
			users_tmp.remove(ctx.message.author.name)
			message = '{0}, {1}. {2}: {3}'.format(ctx.message.author.mention, _('rr', 'you-lose'), _('messages', 'result'), shot_tmp)
			await self.bot.say(message)
		else:
			message = '{0}, {1}. {2}: {3}'.format(ctx.message.author.mention, _('rr', 'next-shot'), _('messages', 'result'), shot_tmp)
			await self.bot.say(message)

		if len(users_tmp) == 1:
			message = '{0}, {1}. {2}: {3}'.format(ctx.message.author.mention, _('rr', 'you-win'), _('messages', 'result'), shot_tmp)
			await self.bot.say(message)

	@rr.command(pass_context=True)
	async def limit(self, ctx, limit:int):
		room = self.users[ctx.message.author.name]

		if ctx.message.author.name in self.rooms[room]['players']:
			if ctx.message.author.name == self.rooms[room]['owner']:
				self.rooms[room]['players'] = self.rooms[room]['players'][0:limit]
				self.rooms[room]['limit'] = limit
				# self.embed.title = '"{0}": {1} {2}'.format(room, _('messages', 'user-limit-changed'), limit)
				self.embed.title = f"{room}: {_('messages', 'user-limit-changed')} from {self.rooms[room]} to {limit}"
				self.embed.color = COLORS["orange"]
				await self.bot.say(embed=self.embed)
			else:
				await self.bot.say(f'{ctx.message.author.mention}, access denied!')

	@rr.command(pass_context=True)
	async def bullets(self, ctx, bullets:int):
		room = self.users[ctx.message.author.name]

		if ctx.message.author.name in self.rooms[room]['players']:
			if ctx.message.author.name == self.rooms[room]['owner']:
				self.embed.title = f"{room}: {_('rr', 'bullets-limit-changed')} from {self.rooms[room]} to {bullets}"
				self.embed.color = COLORS["orange"]
				self.rooms[room]['bullets'] = bullets
				await self.bot.say(embed=self.embed)
			else:
				await self.bot.say(f"{ctx.message.author.mention}, {_('rr', 'access-denied')}")

	@rr.command(pass_context=True)
	async def players(self, ctx):
		self.embed.color = COLORS["drk_blue"]
		for i in self.rooms.keys():
			self.embed.title = '%s - %s' % (_('rr', 'room-info-header'), i)
			self.embed.add_field(name=_('rr', 'owner'), value=self.rooms[i]['owner'])
			self.embed.add_field(name=_('rr', 'players'), value='\n'.join(self.rooms[i]['players']))
			self.embed.add_field(name=_('rr', 'limit'), value=self.rooms[i]['limit'])
		await bot.say(embed=self.embed)

	@rr.command(pass_context=True)
	async def info(self, ctx):
		room = self.users[ctx.message.author.name]
		self.embed.title = title='"{}"'.format(self.rooms[room]['name'])
		self.embed.color = COLORS["drk_blue"]
		self.embed.add_field(name=_('rr', 'owner', case=3), value=self.rooms[room]['owner'])
		self.embed.add_field(name=_('rr', 'limit', case=3), value=self.rooms[room]['limit'])
		self.embed.add_field(name=_('rr', 'players', case=3), value='\n'.join(self.rooms[room]['players']))
		await self.bot.say(embed=self.embed)

	@rr.command(aliases=['del', 'close'], pass_context=True)
	async def delete(self, ctx):
		room = self.users[ctx.message.author.name]

		if ctx.message.author.name in self.rooms[room]['players']:
			if ctx.message.author.name == self.rooms[room]['owner']:
				del self.rooms[room]
				# await self.bot.say('{0}, {1}'.format(ctx.message.author.mention, _('rr', 'room-was-deleted')))
				await self.bot.say(f"{ctx.message.author.mention}, {_('rr', 'room-was-deleted')}")
			else:
				embed = discord.Embed(
					title=_('main', 'help-header').capitalize(),
					color=COLORS["drk_magenta"],
				)				
				embed.title = f"{ctx.message.author.mention}, {_('rr', 'not-a-owner')}"
				embed.color = COLORS["drk_red"]
				await self.bot.say(embed=embed)


def setup(bot):
	bot.add_cog(Games(bot))