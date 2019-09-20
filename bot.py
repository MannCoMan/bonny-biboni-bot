"""
Main module (as a mod)
"""
import os
import time
import random
import datetime
import asyncio

import discord
from discord.ext import commands

from Core.constants import Const
from Core.translate import Translate
from Core.tools import logger

from Core.sql import get_guilds
from Core.sql import insert

tr = Translate("Locales").get
logger = logger("bot")


class Bot(commands.Bot):
    Const = Const()

    def __init__(self, *args, **kwargs):
        super().__init__(
            command_prefix=self._get_prefix,
            case_insensitive=self.Const.BOT_CASE_SENSITIVE,
            description="-info"
        )
        self.remove_command(self.Const.BOT_REMOVED_COMMANDS)

        for mod in self.Const.MODS:
            try:
                self.load_extension(mod)
                print("Mod was loaded - {}".format(mod))
            except discord.ext.commands.errors.ExtensionNotLoaded as err:
                message = "Failed to load {}\n{}: {}".format(mod, type(mod).__name__, err)
                logger.warning(message)

        for folder in self.Const.FOLDERS:
            if not os.path.exists(folder):
                os.makedirs(folder)

        token = kwargs.get("token")
        if not token:
            raise RuntimeError("Can't get token get token")
        self.run(token)

    def _get_prefix(self, bot, ctx):
        guild = ctx.guild.id
        guild, lc, prefix = get_guilds(gid=guild)[0]
        return [prefix, self.Const.BOT_DEFAULT_PREFIX]

    async def _set_tasks(self):
        status = self.Const.BOT_GAME_STATUSES
        timer = self.Const.BOT_STATUS_TIMER

        if self.Const.BOT_ENABLE_DEV_MODE:
            status = self.Const.BOT_DEV_STATUSES
            timer = 1

        game = discord.Game(name=random.choice(status))

        while True:
            await self.change_presence(
                status=discord.Status.online,
                activity=game,
            )
            await asyncio.sleep(timer)

    async def on_guild_join(self, ctx):
        guild = ctx.message.guild.id
        insert(gid=guild, lc=self.Const.BOT_DEFAULT_LOCALE, prefix=self.Const.BOT_DEFAULT_PREFIX)
        message = random.choice(self.Const.BOT_GREET_MESSAGES)
        await ctx.send(tr(message, ctx=ctx, emoji=True))

    async def on_command(self, ctx):
        channel = self.Const.BOT_LOG_CHANNELS.get("on-command-error", None)
        if channel:
            guild = self.get_channel(channel)

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

            await guild.send(embed=embed)

    async def on_command_error(self, ctx, err):
        channel = self.Const.BOT_LOG_CHANNELS.get("on-command-error", None)
        if channel:
            guild = self.get_channel(
                self.Const.BOT_LOG_CHANNELS['on-command-error']
            )

            embed = discord.Embed(
                title=tr("Author", ctx=ctx),
                description="{} - {}".format(ctx.message.author, ctx.message.guild),
                timestamp=datetime.datetime.fromtimestamp(time.time())
            )

            if isinstance(err, commands.CommandOnCooldown):
                message = tr("Please, wait", ctx=ctx, emoji="clock1", member=ctx.message.author.mention)
                embed.add_field(name=tr("Command", ctx=ctx), value=message, inline=True)
                await guild.send(embed=embed)

            if isinstance(err, commands.UserInputError):
                message = tr("Invalid input", ctx=ctx, emoji="warning", err=ctx.command)
                embed.add_field(name=tr("Command", ctx=ctx), value=message, inline=True)
                await guild.send(embed=embed)

            if isinstance(err, commands.BadArgument):
                message = tr("Bad command argument in", emoji="warning", err=ctx.command.content)
                embed.add_field(name=tr("Command", ctx=ctx), value=message, inline=True)
                await guild.send(embed=embed)

            if isinstance(err, commands.CommandNotFound):
                message = tr("Command not found", ctx=ctx, emoji="warning", err=ctx.message.content)
                embed.add_field(name=tr("Command", ctx=ctx), value=message, inline=True)
                await guild.send(embed=embed)

            if isinstance(err, UnboundLocalError):
                message = "Hidden error: {}".format(err)
                embed.add_field(name=tr("Command", ctx=ctx), value=message, inline=True)
                await guild.send(embed=embed)

    async def on_ready(self):
        print("bot login: {}\nbot id: {}\n".format(
            self.user.name,
            self.user.id
        ))
        self.loop.create_task(self._set_tasks())
