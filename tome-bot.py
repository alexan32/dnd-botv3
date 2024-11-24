import config.config as config
import discord
import argparse

from discord.ext import commands


# GET ENVIRONMENT VALUES
parser = argparse.ArgumentParser()
parser.add_argument('--stage', required=False, default="dev")
stage = parser.parse_args().stage
config.init(stage)

token = config.ENVIRONMENT["token"]
logHandler = config.HANDLER
logger = config.LOGGER

# CONFIGURE BOT INTENTS
intents = discord.Intents(
    messages=True,
    guilds=True,
    members=True
)
intents.message_content = True

# CONFIGURE BOT COMMANDS
bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command('help')

@bot.command(
    brief="Get help with bot commands."
)
async def help(ctx, command_name: str=None):
    await ctx.message.delete()
    if command_name is None:
        commands_list = '\n'.join([f"- {cmd.name}:".ljust(20) + str(cmd.short_doc) for cmd in bot.commands])
        help_message = f"=====Help Menu=====\n\n{commands_list}\n\nFor more details type \"!help <command>\""
        await ctx.send(f"```{help_message}```", delete_after=120)
    else:
        command = bot.get_command(command_name)
        if command:
            await ctx.send(f"```{command.help}```", delete_after=120)
        else:
            await ctx.send(f"```No command called {command_name} found.```", delete_after=15)

LOADED = False

@bot.event
async def on_ready():
    
    if not LOADED:
        logger.info("loading bot extensions.")
        await bot.load_extension("bot_extensions.CharacterManagement")
        await bot.load_extension("bot_extensions.Command")
        logger.info("======= BOT IS READY! =======")
        LOADED = True

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("```Command not found! Use \"!help\" to see a list of valid commands.```")
    else:
        logger.error(error)
        await ctx.send("```Oops! Something went wrong.```", delete_after=60)

# LAUNCH BOT
bot.run(config.ENVIRONMENT["token"], log_handler=logHandler)