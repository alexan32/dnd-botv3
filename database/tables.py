import os
import json
from tinydb import TinyDB, Query
from uuid import uuid4
from config.config import ENVIRONMENT, LOGGER
Row = Query()

script_dir = os.path.dirname(__file__)
logger = LOGGER

def get_active_character(discordId, user_table, character_table):
    status = 200
    message = "ok"
    data = None

    _status, _, user = user_table.get_user(discordId)
    if _status == 404:
        return 404, "You are not yet registered as a user. See !help to get started.", None
    elif _status != 200:
        return 400, "Encountered an issue. Please try again later.", None
    

    first = user["activeCharacter"]
    if not first:
        return 400, "You don't have a character currently selected. See !help to get started.", data
    
    status, message, character = character_table.get_character(discordId, first)
    return status, message, character


# wrapper for user table
class LocalUserTable:

    def __init__(self):
        self.table = TinyDB(os.path.join(script_dir, 'users.json'))

    def get_user(self, discordId):
        status = 200
        message = "ok"
        data = None

        character = self.table.get((Row.discordId == discordId))
        if not character:
            status = 404
            message = "Not found"

        return status, message, character
    
    def put_user(self, user_data:dict):
        self.table.upsert(user_data, (Row.discordId == user_data["discordId"]))

        return 200, "ok", None
    
    def set_active_character(self, discordId, first):
        status, message, user_data = self.get_user(discordId)
        if status != 200:
            return status, message, None
        
        user_data["activeCharacter"] = first
        return self.put_user(user_data)

    def create_user(self, discordId):
        status = 200
        message = "ok"

        user_data = {
            "discordId": discordId,
            "activeCharacter": None
        }
        self.table.upsert(user_data, (Row.discordId == discordId))

        return status, message, user_data


class LocalCharacterTable:

    def __init__(self):
        self.table = TinyDB(os.path.join(script_dir, 'characters.json'))

    def create_character(self, discordId, first, last, template="5e"):
        status = 200
        message = "ok"
        data = None

        # check for existing character
        character = self.table.get((Row.discordId == discordId) & (Row.first == first))
        if character:
            return 400, f"You already have a character with first name \"{first}\".", data
        
        # validation
        if template not in ["5e", "min"]:
            return 404, f"Template \"{template}\" is not valid.", data
        
        # add character
        with open(os.path.join(script_dir, f'templates/{template}.json')) as f:
            character_data = json.load(f)
        character_data["discordId"] = discordId
        character_data["first"] = first
        character_data["last"] = last
        self.table.upsert(character_data, ((Row.discordId == discordId) & (Row.first == first)))

        return status, f"character \"{first} {last}\" created.", character_data

    def get_character(self, discordId, first):
        status = 200
        message = "ok"
        character = None

        character = self.table.get((Row.discordId == discordId) & (Row.first == first))
        if not character:
            return 404, f"Found no character \"{first}\".", None

        return status, message, character

    def get_player_characters(self, discordId):
        search_results = self.table.search((Row.discordId == discordId))
        
        def mapping(input):
            return {
                "first": input['first'],
                "last": input['last']
            }
    
        results = list(map(mapping, search_results))
        return 200, "ok", results

    def update_character(self, character_data):
        status = 200
        message = "ok"
        data = None

        self.table.upsert(character_data, ((Row.discordId == character_data['discordId']) & (Row.first == character_data['first'])))

        return status, message, data
