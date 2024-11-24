from discord.ext import commands
import config.config as config
import services.command as command
from .util import delete_after
from .HelpText import *

logger = config.LOGGER

class Command(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        logger.info("Command extension init")

    @commands.command(
        brief="Create, list, search, delete, or modify counters.",
        help=counter_long
    )
    async def counter(self, ctx, *args):

        discordId = ctx.author.id
        _input = "counter " + " ".join(args)
        
        responses = command.command_handler(discordId, _input)
        
        for response in responses:
            await ctx.send(f"```{response}```", delete_after=60)
        await delete_after(ctx, 10.0)

    @commands.command(
        brief="View, edit, search, or delete \"composite\" rolls.",
        help=composite_long
    )
    async def composite(self, ctx, *args):

        discordId = ctx.author.id

        _input = "composite " + " ".join(args)
        
        responses = command.command_handler(discordId, _input)
        
        for response in responses:
            await ctx.send(f"```{response}```", delete_after=60)
        await delete_after(ctx, 10.0)


    @commands.command(
        brief="execute saved command macros",
        help=func_long,
        aliases=["macro", "function"]
    )
    async def func(self, ctx, *args):

        discordId = ctx.author.id

        _input = "func " + " ".join(args)
        
        responses = command.command_handler(discordId, _input)
        
        for response in responses:
            await ctx.send(f"```{response}```")
        await delete_after(ctx, 10.0)


    @commands.command(            
        brief="View, edit, search, or delete character \"rolls\"",
        help=roll_long
    )
    async def roll(self, ctx, first_arg, *args):

        discordId = ctx.author.id

        _input = "roll " + first_arg + " " + " ".join(args)
        
        responses = command.command_handler(discordId, _input)
        
        if first_arg in ["list", "search", "delete"]:
            for response in responses:
                await ctx.send(f"```{response}```", delete_after=120)
        else:

            status, message, character = command.get_active_character(discordId, command.user_table, command.character_table)
            first = character['first']
            last = character['last']

            for response in responses:
                await ctx.send(f"```{first} {last} rolled {response}```")
        await delete_after(ctx, 10.0)

        
async def setup(bot):
    await bot.add_cog(Command(bot))