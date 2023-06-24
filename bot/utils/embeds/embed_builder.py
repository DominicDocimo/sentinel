from config import version, build_stability
import discord


class EmbedBuilder:
    """Contains functions returning pre-built embeds."""
    def __init__(self, custom_footer: str = None):
        self.footer = EmbedUtils.select_footer(custom_footer)

    def unhandled_exception_report(self, ctx: discord.ApplicationContext, exc: discord.DiscordException):
        embed = discord.Embed(title="Application Error Report", description=f"```{exc}```", color=discord.Color.red())
        embed.add_field(name="Version", value=f"{version} ({build_stability})", inline=False)
        embed.add_field(name="Guild", value=f"{ctx.guild.id}", inline=False)
        embed.add_field(name="Author", value=f"<@{ctx.author.id}>", inline=False)
        embed.set_footer(text=self.footer)
        return embed


class EmbedUtils:
    """Utility functions for class EmbedBuilder."""
    @staticmethod
    def select_footer(custom_footer: str = None):
        if custom_footer:
            return custom_footer
        elif build_stability == "stable":
            return f"Running Sentinel v{version}. Please report any errors in our support server."
        else:
            return f"Running an unstable version of Sentinel ({build_stability}). It is not recommended to use this " \
                   f"build for non-testing purposes."
