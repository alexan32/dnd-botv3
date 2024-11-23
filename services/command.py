from .cmd_handler import execute
from . import cache_svc
from . import database
from config.config import UPDATE_FLAG
import json


def getCharacterData(participant, guildId):
    characterData = cache_svc.fetchCharacter(participant, guildId)
    if characterData:
        print(f"found character data in cache")
    else:
        print(f"character data not in cache, fetching from data svc")
        status, characterData = database.fetchCharacter(participant, guildId)
    return characterData

def updateCharacter(participant, guildId, characterData:dict):
    if characterData.get(UPDATE_FLAG, False):
        del characterData[UPDATE_FLAG]
        cache_svc.storeCharacter(participant, guildId, characterData)
        status, message =database.updateCharacter(characterData)
        return status, [message]
    return 200, []

if __name__ == "__main__":
    print(execute("roll 1d20 + 7", {}))