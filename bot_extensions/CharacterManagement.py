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

class CharacterManagement(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        logger.info("character management extension init")

    # give info about user. current character and list of characters.
    @commands.command()
    async def characters(self, ctx, *args):
        await ctx.message.delete()
        discord_id = ctx.author.id
        message = command.aboutme(discord_id) 
        await ctx.send(message, delete_after=15.0)

    # register new user 
    @commands.command()
    async def register(self, ctx, *args):
        await ctx.message.delete()
        discord_id = ctx.author.id
        message = command.register(discord_id)
        await ctx.send(message, delete_after=15.0)

    # switch between characters
    @commands.command()
    async def playas(self, ctx, first, *args):
        await ctx.message.delete()
        discord_id = ctx.author.id
        message = command.playas(discord_id, first)
        await ctx.send(message, delete_after=15.0)

    # create new character
    @commands.command()
    async def create(self, ctx, first, last, *args):
        await ctx.message.delete()
        discord_id = ctx.author.id
        template = "5e"
        if len(args) > 1:
            template = args[0]

        message = command.create_character(discord_id, first, last, template)
        await ctx.send(message, delete_after=15.0)

    # download current character as JSON doc
    @commands.command()
    async def download(self, ctx, *args):
        await ctx.message.delete()
        participant = ctx.author.id
        status, message, characterData = command.get_active_character(participant, command.user_table, command.character_table)
        if status != 200:
            await ctx.send(message, delete_after=15.0)
            return
        first = characterData["first"]
        last = characterData["last"]
        fileName = f"{first}-{last}.json"
        f = open(fileName, 'w')
        f.write(json.dumps(characterData))
        f.close()
        f = open(fileName, 'r')
        await ctx.send("This file will be accessible for 1 minute.", file=discord.File(f), delete_after=60.0)
        f.close()
        os.remove(fileName)

    # overwrite current character with JSON doc
    @commands.command()
    async def upload(self, ctx):
        discord_id = ctx.author.id
        try:
            attachment_url = ctx.message.attachments[0].url
            file_request = requests.get(attachment_url)
            contents = json.loads(file_request.content.decode("utf-8"))
            contents["discordId"] = str(discord_id)
            contents[UPDATE_FLAG] = True
            first = contents['first']
            last = contents['last']
        except Exception as e:
            print(e)
            await ctx.send(f"```Failed to process file. Make sure that you attach a valid character JSON file before sending.```", delete_after=60.0)
        else:
            status, message, data = command.character_table.update_character(contents)
            if status != 200:
                await ctx.send(f"```{status}. {message}```", delete_after=60.0)
            else:
                await ctx.send(f"```Saved \"{first} {last}\" successfully.```", delete_after=60.0)
                
        await ctx.message.delete()
        
async def setup(bot):
    await bot.add_cog(CharacterManagement(bot))