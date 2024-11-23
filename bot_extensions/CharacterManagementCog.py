# This extension is used to associate discord users/guilds with the appropriate
# user data in the back end. 
#

import discord
from discord.ext import commands
import config.config as config
from services import command
import json
import os
import requests
from config.config import UPDATE_FLAG
logger = config.LOGGER

class CharacterManagementCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        logger.info("character management extension init")

    # give info about current character
    @commands.command()
    async def me(self, ctx, *args):
        await ctx.message.delete()    

    # register new user 
    @commands.command()
    async def register(self, ctx, *args):
        await ctx.message.delete()

    # switch between characters
    @commands.command()
    async def playas(self, ctx, *args):
        await ctx.message.delete()

    # create new character
    @commands.command()
    async def create(self, ctx, *args):
        await ctx.message.delete()    

    # download current character as JSON doc
    @commands.command()
    async def download(self, ctx, *args):
        await ctx.message.delete()
        
        participant = ctx.author.id
        guildId = ctx.guild.id

        characterData = command.getCharacterData(participant, guildId)
        first = characterData["meta"]["first"]
        last = characterData["meta"]["last"]
        fileName = f"{first}-{last}.json"
        f = open(fileName, 'w')
        f.write(json.dumps(characterData))
        f.close()
        f = open(fileName, 'r')
        await ctx.send(file=discord.File(f), delete_after=60.0)
        await ctx.message.delete()
        f.close()
        os.remove(fileName)

    # overwrite current character with JSON doc
    @commands.command()
    async def upload(self, ctx):
        participant = ctx.author.id
        guildId = ctx.guild.id
        try:
            attachment_url = ctx.message.attachments[0].url
            file_request = requests.get(attachment_url)
            contents = json.loads(file_request.content.decode("utf-8"))
            contents["participant"] = str(participant)
            contents[UPDATE_FLAG] = True
        except Exception as e:
            print(e)
            await ctx.send(f"```Failed to process file. Make sure that you attach a valid character JSON file before sending.```", delete_after=60.0)
        else:
            print(contents)
            status, messages = command.updateCharacter(participant, guildId, contents)
            if status != 200:
                for message in messages:
                    await ctx.send(f"```{status}. {messages[0]}```", delete_after=60.0)
                    await ctx.message.delete()
        await ctx.message.delete()
        
async def setup(bot):
    await bot.add_cog(CharacterManagementCog(bot))
