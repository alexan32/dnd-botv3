import json
import requests
from config.config import ENVIRONMENT, LOGGER

logger = LOGGER


def fetchParticipant(guildId, discordId):

    url = ENVIRONMENT["participantServiceEndpoint"]
    response = requests.get(url, json={"guildId": guildId, "discordId":discordId})
    logger.debug(f"PUT Response from character service: {response.status_code}")

    status = response.status_code
    if status != 200:
        logger.error(response.text)
        message = "Failed to fetch participant data. Please try again later"
    return status, message

def fetchCharacter(characterId):
    logger.info("fetching character from database")
    status = 200
    message = "ok"
    
    url = ENVIRONMENT["characterServiceEndpoint"]
    response = requests.get(url, json={"characterId": characterId})
    logger.debug(f"PUT Response from character service: {response.status_code}")

    status = response.status_code
    if status != 200:
        logger.error(response.text)
        message = "Failed to update character data. Please try again later"

    return status, message

def updateCharacter(chararacterData:dict):
    logger.info("performing character update")
    status = 200
    message = "ok"
    
    url = ENVIRONMENT["characterServiceEndpoint"]
    response = requests.put(url, json=chararacterData)
    logger.debug(f"PUT Response from character service: {response.status_code}")

    status = response.status_code
    if status != 200:
        logger.error(response.text)
        message = "Failed to update character data. Please try again later"
    return status, message

