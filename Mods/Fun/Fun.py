import discord
from discord.ext import commands

import os
import re
import random
import datetime
import requests

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from pyfiglet import figlet_format
from imgurpython import ImgurClient

import wand.image as image
from wand.display import display

from io import BytesIO
from Core.Settings import *
from Core.Wrapper import Wrapper, Translate


get = Wrapper("Configs/Fun.json").get
_ = Translate("Mods", "Fun", "Locales").get


class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		self.imgur_client = ImgurClient(
			IMGUR_CLIEND_ID,
			IMGUR_CLIENT_SECRET
		)

	@commands.command(aliases=_("aliases", "spongebob"), pass_context=True)
	@commands.cooldown(1, 3, commands.BucketType.user)
	async def spongebob(self, ctx):
		await self._blend_images(
			ctx=ctx,
			filename="spongebob1.png",
			attachments=ctx.message.attachments,
			bg_size=(399, 299),
			bg_coord=(97, 305)
		)

	@commands.command(aliases=_("aliases", "ihadtogrind"), pass_context=True)
	@commands.cooldown(1, 3)
	async def ihadtogrind(self, ctx):
		await self._blend_images(
			ctx=ctx,
			filename="ihadtogrind.png",
			attachments=ctx.message.attachments,
			bg_size=(545, 531),
			bg_coord=(15, 64),
		)

	@commands.command(aliases=_("aliases", "granpatv"), pass_context=True)
	@commands.cooldown(1, 3)
	async def granpatv(self, ctx):
		await self._blend_images(
			ctx=ctx,
			filename="granpatv.png",
			attachments=ctx.message.attachments,
			bg_size=(430, 243),
			bg_coord=(45, 253),
		)

	@commands.command(aliases=_("aliases", "mrkrupp"), pass_context=True)
	@commands.cooldown(1, 3)
	async def mrkrupp(self, ctx):
		await self._blend_images(
			ctx=ctx,
			filename="mrkrupp.png",
			attachments=ctx.message.attachments,
			bg_size=(566, 418),
			bg_coord=(0, 0),
		)

	@commands.command(aliases=_("aliases", "spore"), pass_context=True)
	@commands.cooldown(1, 3)
	async def spore(self, ctx):
		await self._blend_images(
			ctx=ctx,
			filename="spore.png",
			attachments=ctx.message.attachments,
			bg_size=(1024, 1024),
			bg_coord=(0, 0),
		)

	@commands.command(aliases=_("aliases", "spywow"), pass_context=True)
	@commands.cooldown(1, 3)
	async def spywow(self, ctx):
		await self._blend_images(
			ctx=ctx,
			filename="spywow.png",
			attachments=ctx.message.attachments,
			bg_size=(600, 339),
			bg_coord=(0, 0),
		)

	@commands.command(aliases=_("aliases", "thisguy"), pass_context=True)
	@commands.cooldown(1, 3)
	async def thisguy(self, ctx):
		await self._blend_images(
			ctx=ctx,
			filename="thisguy.png",
			attachments=ctx.message.attachments,
			bg_size=(520, 451),
			bg_coord=(0, 191),
		)

	@commands.command(aliases=_("aliases", "thiswoman"), pass_context=True)
	@commands.cooldown(1, 3)
	async def thiswoman(self, ctx):
		await self._blend_images(
			ctx=ctx,
			filename="thiswoman.png",
			attachments=ctx.message.attachments,
			bg_size=(964, 467),
			bg_coord=(0, 444),
		)

	@commands.command(aliases=_("aliases", "icecream"), pass_context=True)
	@commands.cooldown(1, 3)
	async def icecream(self, ctx):
		await self._blend_images(
			ctx=ctx,
			filename="icecream.png",
			attachments=ctx.message.attachments,
			bg_size=(309, 261),
			bg_coord=(202, 250),
		)

	@commands.command(aliases=_("aliases", "obstetrician"), pass_context=True)
	@commands.cooldown(1, 3)
	async def obstetrician(self, ctx):
		await self._blend_images(
			ctx=ctx,
			filename="obstetrician.png",
			attachments=ctx.message.attachments,
			bg_size=(962, 727),
			bg_coord=(22, 13),
		)

	@commands.command(aliases=_("aliases", "anus"), pass_context=True)
	@commands.cooldown(1, 3)
	async def anus(self, ctx):
		await self._blend_images(
			ctx=ctx,
			filename="anus.png",
			attachments=ctx.message.attachments,
			bg_size=(225, 191),
			bg_coord=(0, 0),
		)

	@commands.command(aliases=_("aliases", "dream"), pass_context=True)
	@commands.cooldown(1, 3)
	async def dream(self, ctx):
		await self._blend_images(
			ctx=ctx,
			filename="dream.png",
			attachments=ctx.message.attachments,
			bg_size=(685, 450),
			bg_coord=(0, 308),
		)		

	@commands.command(aliases=_("aliases", "slam"), pass_context=True)
	@commands.cooldown(1, 3)
	async def slam(self, ctx):
		await self._blend_images(
			ctx=ctx,
			filename="slam.png",
			attachments=ctx.message.attachments,
			bg_size=(315, 447),
			bg_coord=(338, 14),
		)

	# @commands.command(aliases=_("aliases", "skibidi"), pass_context=True)
	# @commands.cooldown(1, 3)
	# async def skibidi(self, ctx):
		# pass

	@commands.command(aliases=_("aliases", "badmeme"), pass_context=True)
	@commands.cooldown(1, 3)
	async def badmeme(self, ctx):
		try:
			req = requests.get("https://api.imgflip.com/get_memes")
			await ctx.send(random.choice(req.json()["data"]["memes"])["url"])
		except Exception as e:
			print(e)

	@commands.command(aliases=_("aliases", "magic"), pass_context=True)
	@commands.cooldown(2, 5, commands.BucketType.user)
	# Forked from `NotSoBot`
	async def magic(self, ctx, scale=3):
		try:
			if scale > 10:
				await ctx.send(_("error-magic-max-value"))
				scale = 1

			to_send = "Images/Temp/magic.png"
			url = await self._get_images(ctx)

			response = requests.get(url)
			img = Image.open(BytesIO(response.content))
			img.save(to_send, "PNG")
			img = image.Image(filename=to_send)

			img.liquid_rescale(
				width=int(img.width * 0.5), 
				height=int(img.height * 0.5), 
				delta_x=int(0.5 * scale) if scale else 1, 
				rigidity=0)

			img.liquid_rescale(
				width=int(img.width * 1.5), 
				height=int(img.height * 1.5), 
				delta_x=scale if scale else 2,
				rigidity=0)		
			img.save(filename=to_send)

			await ctx.send(file=discord.File(to_send))
			os.remove(to_send)
		except Exception as e:
			await ctx.send(_("error-base-exception").format(e))

	@commands.command(aliases=_("aliases", "impact-meme"), pass_context=True)
	async def impact_meme(self, ctx, *string):
		# Forked from: https://github.com/Littlemansmg/Discord-Meme-Generator
		# Get image from URL
		await ctx.trigger_typing()

		to_send = "Images/Temp/meme.png"
		location = await self._get_images(ctx)
		response = requests.get(location)			
		font_path = FONTS["impact"]

		if len(string):
			string_size = len(string) // 2
			top_string = " ".join(string[:string_size])
			bottom_string = " ".join(string[string_size:])

			with Image.open(BytesIO(response.content)) as img:
				size = img.size
				font_size = int(size[1] / 5)
				# font = IFont.truetype(font=font_path, size=font_size)
				font = ImageFont.truetype(font_path, font_size)
				edit = ImageDraw.Draw(img)

				# find biggest font size that works

				top_text_size = font.getsize(top_string)
				bottom_text_size = font.getsize(bottom_string)

				while top_text_size[0] > size[0] - 20 or bottom_text_size[0] > size[0] - 20:
					font_size = font_size - 1
					font = ImageFont.truetype(font_path, font_size)
					top_text_size = font.getsize(top_string)
					bottom_text_size = font.getsize(bottom_string)

				# find top centered position for top text
				top_text_posx = (size[0] / 2) - (top_text_size[0] / 2)
				top_text_posy = 0
				top_text_pos = (top_text_posx, top_text_posy)

				# find bottom centered position for bottom text
				bottom_text_posx = (size[0] / 2) - (bottom_text_size[0] / 2)
				bottom_text_posy = size[1] - bottom_text_size[1] - 10
				bottom_text_pos = (bottom_text_posx, bottom_text_posy)

				# draw outlines
				# there may be a better way
				outline_range = int(font_size / 15)
				for x in range(-outline_range, outline_range + 1):
					for y in range(-outline_range, outline_range + 1):
						edit.text((top_text_pos[0] + x, top_text_pos[1] + y), top_string, (0, 0, 0), font=font)
						edit.text((bottom_text_pos[0] + x, bottom_text_pos[1] + y), bottom_string, (0, 0, 0), font=font)

				edit.text(top_text_pos, top_string, (255, 255, 255), font=font)
				edit.text(bottom_text_pos, bottom_string, (255, 255, 255), font=font)
				img.save(to_send, "PNG")

			await ctx.send(file=discord.File(to_send))
			os.remove(to_send)
		else:
			await ctx.send(_("error-text-is-empty"))

	async def _blend_images(self, ctx:str, filename:str, **kwargs):
		"""
		Keyword arguments for "_blend_images" method:
		* filename       - background image path
		* attachments    - attached urls, default - None
		* bg_size        - background image width and height, default - (None, None)
		* bg_coord       - background image coordinates, default - (None, None)
		* bg_scale_x1    - rescale image by x1, default - 0
		* bg_scale_y1    - rescale image by y1, default - 0
		* bg_scale_x2    - rescale image by x2, default - 0
		* bg_scale_y2    - rescale image by y2, default - 0
		* bg_resize_w    - resize image width, default - 0
		* bg_resize_h    - resize image height, default - 0
		"""

		await ctx.trigger_typing()
		
		to_send = f"Images/Temp/{filename}"
		w, h = kwargs.get("bg_size", None)
		x, y = kwargs.get("bg_coord", None)
		response = await self._get_images(ctx)
		response = requests.get(response)

		foreground = os.path.join(IMAGES_TEMPLATE_PATH, filename)
		foreground = Image.open(foreground)

		background = Image.open(BytesIO(response.content))
		if 3000 in background.size:
			await ctx.send(f":warning: Image is too large - `{background.size[0]}x{background.size[1]}`!")
		else:
			background = background.resize((w, h))

			blended = Image.new("RGBA", foreground.size)
			blended.paste(background, (x, y))
			blended.paste(foreground, (0, 0), foreground)
			blended.save(to_send, "PNG")

			await ctx.send(file=discord.File(to_send))
			os.remove(to_send)

	async def _circulate_image(self, image:Image.Image, radius:int):
		pass

	async def _save_image(self, url, ext="png"):
		name = url.split("/")[-1]
		name = name.split(".")[0]
		name = "Images/Temp/{}.{}".format(name, ext)

		response = requests.get(url)
		image = Image.open(BytesIO(response.content))
		image.save(name)
		return name if name else await ctx.send(_("error-cant-download-image").format(url))

	async def _get_images(self, ctx, **kwargs):
		limit = kwargs.get("history_limit", 200)

		async for c in ctx.history(limit=limit): # limit=10
			if len(c.attachments) > 0:
				background_url = c.attachments[0].url
				background_ext = background_url.split(".")[-1]
				return background_url if background_ext in ("png", "gif", "jpeg", "jpg") else None

	@commands.command(aliases=_("aliases", "whois"), pass_context=True)
	async def whois(self, ctx, *text):
		try:
			if text is None:
				text = "гей"

			member = await self._get_all_members(ctx)
			member = random.choice(member)
			await ctx.send(_("whois-text").format(member))

		except Exception as e:
			await ctx.send(_("error-base-exception").format(e))

	async def _get_all_members(self, ctx, no_bots=False):
		collect = []
		for member in ctx.guild.members:
			collect.append(member.name)
		return collect

	@commands.command(aliases=_("aliases", "imgur"), pass_context=True)
	@commands.cooldown(2, 5)
	async def imgur(self, ctx, text:str=None):
		try:
			if text is None:
				load = self.imgur_client.gallery_random(page=0)
			else:
				load = self.imgur_client.gallery_search(text, advanced=None, sort="viral", window="all", page=0)
			rand = random.choice(load)
			try:
				if "image/" in rand.type:
					await ctx.send(f"{rand.link}")
			except AttributeError:
				if rand.title:
					title = f"**{rand.title}**\n"
				else:
					title = ""
				await ctx.send(f"{title}{rand.link}")

		except Exception as e:
			await ctx.send(_("error-base-exception").format(e))

	@commands.command(aliases=_("aliases", "minecraft"), pass_context=True)
	@commands.cooldown(1, 3)
	async def minecraft(self, ctx, *text):
		try:
			if len(text) == 0 :
				text = "Насрал в штаны"
			else:
				text = " ".join(text)

			symbols = (u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
				u"abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA")
			tr = {ord(a) : ord(b) for a, b in zip(*symbols)}
			
			url = "https://mcgen.herokuapp.com/a.php?i=1&h=%s&t=%s" % (text.capitalize().translate(tr), str(ctx.message.author.name).translate(tr))
			response = requests.get(url)
			image = Image.open(BytesIO(response.content))
			image.save("Images/Temp/minecraft.png", "PNG")

			await ctx.send(file=discord.File("Images/Temp/minecraft.png"))
			os.remove("Images/Temp/minecraft.png")

		except Exception as e:
			await ctx.send(_("error-base-exception").format(e))

def setup(bot):
	bot.add_cog(Fun(bot))