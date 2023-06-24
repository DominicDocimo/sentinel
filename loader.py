from discord.ext import commands
from discord.commands import core
from pathlib import Path
from logging import getLogger
from config import developer_server_id
from bot.utils.embeds.embed_builder import EmbedBuilder
from abc import ABC
import discord

log = getLogger(__name__)


class BotLoader(commands.Bot, ABC):
    def __init__(self, *args, **kwargs):
        """Loads bot extensions."""
        super().__init__(*args, **kwargs)

        for ext in Path().glob("bot/cogs/*/*.py"):
            try:
                self.load_extension(".".join(part for part in ext.parts)[:-len(ext.suffix)])
            except discord.ExtensionNotLoaded:
                log.exception(f"Could not load extension {ext}")

    async def on_ready(self):
        """Bot loaded successfully and is ready to be used."""
        log.info(f"Ready: {self.user} (ID: {self.user.id})")

    async def on_application_command_error(self, ctx: discord.ApplicationContext, exc: discord.DiscordException):
        """Handles errors related to application commands."""
        match exc:
            case core.CheckFailure:
                pass
            case discord.NotFound:
                try:
                    await ctx.respond("There was an issue connecting to the Discord API. Please try again.",
                                      ephemeral=True)
                except discord.Forbidden:
                    await ctx.send(str(exc))
                return
            case _:
                await self.get_channel(developer_server_id).send(
                    embed=EmbedBuilder().unhandled_exception_report(ctx, exc))
                log.error("", exc_info=exc)
