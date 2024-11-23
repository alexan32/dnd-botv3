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

    @commands.command()
    async def counter(self, ctx, *args):
        delete_after(ctx, 60.0)

        discordId = ctx.author.id
        _input = "counter " + " ".join(args)
        
        responses = command.command_handler(discordId, _input)
        
        for response in responses:
            await ctx.send(f"```{response}```", delete_after=60)

    @commands.command(
        brief="View, edit, search, or delete \"composite\" rolls.",
        help=composite_long
    )
    async def composite(self, ctx, *args):
        delete_after(ctx, 60.0)

        discordId = ctx.author.id

        _input = "composite " + " ".join(args)
        
        responses = command.command_handler(discordId, _input)
        
        for response in responses:
            await ctx.send(f"```{response}```", delete_after=60)


    @commands.command()
    async def func(self, ctx, *args):
        delete_after(ctx, 60.0)

        discordId = ctx.author.id

        _input = "func " + " ".join(args)
        
        responses = command.command_handler(discordId, _input)
        
        for response in responses:
            await ctx.send(f"```{response}```")


    @commands.command(            
        brief="View, edit, search, or delete character \"rolls\"",
        help=roll_long
    )
    async def roll(self, ctx, first_arg, *args):
        await ctx.message.delete()

        discordId = ctx.author.id

        _input = "roll " + first_arg + " ".join(args)
        
        responses = command.command_handler(discordId, _input)
        
        if first_arg in ["list", "search", "delete"]:
            for response in responses:
                await ctx.send(f"```{response}```", delete_after=120)
        else:
            for response in responses:
                await ctx.send(f"```{response}```")

        
async def setup(bot):
    await bot.add_cog(Command(bot))