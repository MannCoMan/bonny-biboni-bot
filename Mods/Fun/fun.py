import discord
from discord.ext import commands

import os
import random
import datetime
import requests

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from imgurpython import ImgurClient

import wand.image as image
from wand.display import display

from io import BytesIO
from .constants import FunConst
from Core.tools import logger
from Core.translate import Translate


translate = Translate("Mods/Fun/Locales")
tr = translate.get
alias = translate.getalias
logger = logger(__name__)


class Fun(commands.Cog):
    Const = FunConst()

    def __init__(self, bot):
        self.imgur_client = ImgurClient(
            self.Const.IMGUR_CLIENT_ID,
            self.Const.IMGUR_CLIENT_SECRET
        )

    @commands.command(aliases=alias("spongebob"), pass_context=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def spongebob(self, ctx):
        await self._blend_images(
            ctx=ctx,
            filename="spongebob1.png",
            attachments=ctx.message.attachments,
            bg_size=(399, 299),
            bg_coord=(97, 305)
        )

    @commands.command(aliases=alias("ihadtogrind"), pass_context=True)
    @commands.cooldown(1, 3)
    async def ihadtogrind(self, ctx):
        await self._blend_images(
            ctx=ctx,
            filename="ihadtogrind.png",
            attachments=ctx.message.attachments,
            bg_size=(545, 531),
            bg_coord=(15, 64),
        )

    @commands.command(aliases=alias("granpatv"), pass_context=True)
    @commands.cooldown(1, 3)
    async def granpatv(self, ctx):
        await self._blend_images(
            ctx=ctx,
            filename="granpatv.png",
            attachments=ctx.message.attachments,
            bg_size=(430, 243),
            bg_coord=(45, 253),
        )

    @commands.command(aliases=alias("mrkrupp"), pass_context=True)
    @commands.cooldown(1, 3)
    async def mrkrupp(self, ctx):
        await self._blend_images(
            ctx=ctx,
            filename="mrkrupp.png",
            attachments=ctx.message.attachments,
            bg_size=(566, 418),
            bg_coord=(0, 0),
        )

    @commands.command(aliases=alias("spore"), pass_context=True)
    @commands.cooldown(1, 3)
    async def spore(self, ctx):
        await self._blend_images(
            ctx=ctx,
            filename="spore.png",
            attachments=ctx.message.attachments,
            bg_size=(1024, 1024),
            bg_coord=(0, 0),
        )

    @commands.command(aliases=alias("spywow"), pass_context=True)
    @commands.cooldown(1, 3)
    async def spywow(self, ctx):
        await self._blend_images(
            ctx=ctx,
            filename="spywow.png",
            attachments=ctx.message.attachments,
            bg_size=(600, 339),
            bg_coord=(0, 0),
        )

    @commands.command(aliases=alias("thisguy"), pass_context=True)
    @commands.cooldown(1, 3)
    async def thisguy(self, ctx):
        await self._blend_images(
            ctx=ctx,
            filename="thisguy.png",
            attachments=ctx.message.attachments,
            bg_size=(520, 451),
            bg_coord=(0, 191),
        )

    @commands.command(aliases=alias("thiswoman"), pass_context=True)
    @commands.cooldown(1, 3)
    async def thiswoman(self, ctx):
        await self._blend_images(
            ctx=ctx,
            filename="thiswoman.png",
            attachments=ctx.message.attachments,
            bg_size=(964, 467),
            bg_coord=(0, 444),
        )

    @commands.command(aliases=alias("icecream"), pass_context=True)
    @commands.cooldown(1, 3)
    async def icecream(self, ctx):
        await self._blend_images(
            ctx=ctx,
            filename="icecream.png",
            attachments=ctx.message.attachments,
            bg_size=(309, 261),
            bg_coord=(202, 250),
        )

    @commands.command(aliases=alias("obstetrician"), pass_context=True)
    @commands.cooldown(1, 3)
    async def obstetrician(self, ctx):
        await self._blend_images(
            ctx=ctx,
            filename="obstetrician.png",
            attachments=ctx.message.attachments,
            bg_size=(962, 727),
            bg_coord=(22, 13),
        )

    @commands.command(aliases=alias("anus"), pass_context=True)
    @commands.cooldown(1, 3)
    async def anus(self, ctx):
        await self._blend_images(
            ctx=ctx,
            filename="anus.png",
            attachments=ctx.message.attachments,
            bg_size=(225, 191),
            bg_coord=(0, 0),
        )

    @commands.command(aliases=alias("dream"), pass_context=True)
    @commands.cooldown(1, 3)
    async def dream(self, ctx):
        await self._blend_images(
            ctx=ctx,
            filename="dream.png",
            attachments=ctx.message.attachments,
            bg_size=(685, 450),
            bg_coord=(0, 308),
        )

    @commands.command(aliases=alias("slam"), pass_context=True)
    @commands.cooldown(1, 3)
    async def slam(self, ctx):
        await self._blend_images(
            ctx=ctx,
            filename="slam.png",
            attachments=ctx.message.attachments,
            bg_size=(315, 447),
            bg_coord=(338, 14),
        )

    @commands.command(aliases=alias("heroes"), pass_context=True)
    @commands.cooldown(1, 3)
    async def heroes(self, ctx):
        await self._blend_images(
            ctx=ctx,
            filename="heroes.png",
            attachments=ctx.message.attachments,
            bg_size=(428, 412),
            bg_coord=(0, 0),
        )

    @commands.command(aliases=alias("dickgrow"), pass_context=True)
    @commands.cooldown(1, 3)
    async def dickgrow(self, ctx):
        await self._blend_images(
            ctx=ctx,
            filename="dickgrow.jpg",
            attachments=ctx.message.attachments,
            bg_size=(668, 345),
            bg_coord=(0, 0),
        )

    @commands.command(aliases=alias("badmeme"), pass_context=True)
    @commands.cooldown(1, 3)
    async def badmeme(self, ctx):
        try:
            req = requests.get("https://api.imgflip.com/get_memes")
            await ctx.send(random.choice(req.json()["data"]["memes"])["url"])
        except Exception as err:
            print(err)

    @commands.command(aliases=alias("magic"), pass_context=True)
    @commands.cooldown(2, 5, commands.BucketType.user)
    # Forked from `NotSoBot`
    async def magic(self, ctx, scale=3):
        try:
            if scale > 10:
                await ctx.send(tr("The scale argument can't be more than 10", ctx=ctx))
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
            await ctx.send(tr("I pooped myself", ctx=ctx, err=e))

    @commands.command(aliases=alias("impact-meme"), pass_context=True)
    async def impact_meme(self, ctx, *string):
        # Forked from: https://github.com/Littlemansmg/Discord-Meme-Generator
        # Get image from URL
        try:
            await ctx.trigger_typing()

            to_send = "Images/Temp/meme.png"
            location = await self._get_images(ctx)
            response = requests.get(location)
            font_path = self.Const.FONTS["impact"]

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
                            edit.text((bottom_text_pos[0] + x, bottom_text_pos[1] + y), bottom_string, (0, 0, 0),
                                      font=font)

                    edit.text(top_text_pos, top_string, (255, 255, 255), font=font)
                    edit.text(bottom_text_pos, bottom_string, (255, 255, 255), font=font)
                    img.save(to_send, "PNG")

                await ctx.send(file=discord.File(to_send))
                os.remove(to_send)
            else:
                await ctx.send(tr("Type something", ctx=ctx))
        except Exception as err:
            print(err)

    @commands.command(aliases=alias("whois"), pass_context=True)
    async def whois(self, ctx, *text):
        try:
            if text is None:
                text = "гей"

            member = await self._get_members(ctx)
            member = random.choice(member)
            await ctx.send(tr("I think it's a {member}", ctx=ctx, emoji=True, member=member))

        except Exception as err:
            await ctx.send(tr("I pooped myself", ctx=ctx, err=err))

    @commands.command(aliases=alias("when"), pass_context=True)
    async def when(self, ctx):
        try:
            min_year = 1993
            max_year = datetime.datetime.now().year
            start = datetime.datetime(min_year, 1, 1)
            years = max_year - min_year + 1
            end = start + datetime.timedelta(days=365 * years)
            result = start + (end - start) * random.random()
            result = datetime.datetime.strftime(
                result, tr("It happend or will happend in '{tf}'", ctx=ctx, emoji="thinking", tf="%D - %d:%m:%y")
            )
            await ctx.send(result)
        except Exception as err:
            await ctx.send(tr("I pooped myself", ctx=ctx, err=err))

    @commands.command(aliases=alias("imgur"), pass_context=True)
    @commands.cooldown(2, 5)
    async def imgur(self, ctx, text):
        if text is None:
            load = self.imgur_client.gallery_random(page=0)
        else:
            load = self.imgur_client.gallery_search(text, advanced=None, sort="viral", window="all", page=0)
        rand = random.choice(load)
        try:
            if "image/" in rand.type:
                await ctx.send(rand.link)
        except AttributeError:
            if rand.title:
                title = "**{}**\n".format(rand.title)
            else:
                title = ""
            await ctx.send("{}{}".format(title, rand.link))

    @commands.command(aliases=alias("minecraft"), pass_context=True)
    @commands.cooldown(1, 3)
    async def minecraft(self, ctx, *text):
        try:
            if len(text) == 0:
                text = "Насрал в штаны"
            else:
                text = " ".join(text)

            symbols = (
                u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
                u"abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA"
            )

            tr = {ord(a): ord(b) for a, b in zip(*symbols)}

            url = "https://mcgen.herokuapp.com/a.php?i=1&h=%s&t=%s" % (
                text.capitalize().translate(tr),
                str(ctx.message.author.name).translate(tr)
            )

            response = requests.get(url)
            image = Image.open(BytesIO(response.content))
            image.save("Images/Temp/minecraft.png", "PNG")

            await ctx.send(file=discord.File("Images/Temp/minecraft.png"))
            os.remove("Images/Temp/minecraft.png")

        except Exception as err:
            await ctx.send(tr("I pooped myself", ctx=ctx, err=err))

        async def _blend_images(self, ctx,
                                filename=None, attachments=None,
                                bg_size=None, bg_coord=None,
                                bg_scale_x1=None, bg_scale_y1=None,
                                bg_scale_x2=None, bg_scale_y2=None,
                                bg_resize_w=None, bg_resize_h=None):
            """
    		Keyword arguments for "_blend_images" method:
    		Args:
    			filename       - background image path
    			attachments    - attached urls, default
    			bg_size        - background image width and height
    			bg_coord       - background image coordinates
    			bg_scale_x1    - rescale image by x1
    			bg_scale_y1    - rescale image by y1
    			bg_scale_x2    - rescale image by x2
    			bg_scale_y2    - rescale image by y2
    			bg_resize_w    - resize image width
    			bg_resize_h    - resize image height
    		"""

            await ctx.trigger_typing()
            to_send = "Images/Temp/{}".format(filename)

            response = await self._get_images(ctx)
            response = requests.get(response)

            foreground = os.path.join(self.Const.IMAGES_TEMPLATE_PATH, filename)
            foreground = Image.open(foreground)

            background = Image.open(BytesIO(response.content))

            if 3000 in background.size:
                await ctx.send(tr("Image is too large ({w}x{h})", ctx=ctx, w=background.size[0], h=background.size[1]))
            else:
                background = background.resize(bg_size)

                blended = Image.new("RGBA", foreground.size)
                blended.paste(background, bg_coord)
                blended.paste(foreground, (0, 0), foreground)
                blended.save(to_send, "PNG")

                await ctx.send(file=discord.File(to_send))
                os.remove(to_send)

    async def _get_images(self, ctx, history_limit=None, formats=None):
        if not history_limit:
            history_limit = 200

        if not formats:
            formats = ("png", "gif", "jpeg", "jpg")

        async for c in ctx.history(limit=history_limit):  # limit=10
            if len(c.attachments) > 0:
                background_url = c.attachments[0].url
                background_ext = background_url.split(".")[-1]
                return background_url if background_ext in formats else None

    async def _get_members(self, ctx):
        return [i.mention for i in ctx.guild.members]


def setup(bot):
    bot.add_cog(Fun(bot))
