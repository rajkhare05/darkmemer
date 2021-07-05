import discord
from discord.ext import commands

@commands.command(name = 'clear')
async def clear_messages(ctx, channel: discord.TextChannel = None):
    if channel is None:
        channel = ctx.channel
    if channel in ctx.guild.text_channels:
        return await ctx.channel.purge()

def setup(bot):
    bot.add_command(clear_messages)
