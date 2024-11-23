from discord.ext import commands
import config.config as config
import services.command as command


logger = config.LOGGER

class Command(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        logger.info("Command extension init")

        
async def setup(bot):
    await bot.add_cog(Command(bot))