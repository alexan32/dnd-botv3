import json
from .cmd_handler import execute
from config.config import UPDATE_FLAG, LOGGER
from database.tables import (
    LocalUserTable as UserTable, 
    LocalCharacterTable as CharacterTable,
    get_active_character
    )


logger = LOGGER
user_table = UserTable()
character_table = CharacterTable()

GENERIC_ERROR_MESSAGE = "Encountered an issue. Please try again later."

# Join as a user
def register(discordId):
    status, message, data = user_table.get_user(discordId)
    if status == 200:
        return "Your discord account is already registered as a bot user."
    else:
        status, message, data = user_table.create_user(discordId)
        if status == 200:
            return "You have been successfully registered as a bot user."
        else:
            return GENERIC_ERROR_MESSAGE
        
# Create a character
def create_character(discordId, first:str, last:str, template:str="5e"):
    status, message, data = character_table.create_character(discordId, first, last, template)

    return message

# Set your active character
def playas(discordId, first:str):
    status, message, character_data = character_table.get_character(discordId, first)
    if status == 404:
        return message
    elif status != 200:
        return GENERIC_ERROR_MESSAGE
    
    status, message, data = user_table.set_active_character(discordId, first)
    if status != 200:
        return GENERIC_ERROR_MESSAGE
    return f"You are now playing as \"{first} {character_data['last']}\""

# info about user
def aboutme(discordId):
    status, message, user_data = user_table.get_user(discordId)
    if status == 404:
        return "Not yet registered"
    elif status != 200:
        return GENERIC_ERROR_MESSAGE
    status, message, character_list = character_table.get_player_characters(discordId)
    if status != 200:
        return GENERIC_ERROR_MESSAGE
    active_character = user_data['activeCharacter']
    response = f"Active character: {active_character}\nTotal characters: {len(character_list)}"
    for x in character_list:
        response += f"\n- {x['first']} {x['last']}"
    return response

def command_handler(discordId, _input:str):
    status, message, characterData = get_active_character(discordId, user_table, character_table)
    if status != 200:
        return [GENERIC_ERROR_MESSAGE]
    
    messages = []

    try:
        messages = execute(_input, characterData)
    except Exception as e:
        logger.info(f"{discordId} entered \"{_input}\" resulting in {e}")
    else:
        character_table.update_character(characterData)

    return messages

if __name__ == "__main__":
    pass