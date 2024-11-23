import json
import argparse
import config.config as config

# GET ENVIRONMENT VALUES
parser = argparse.ArgumentParser()
parser.add_argument('--stage', required=False, default="dev")
stage = parser.parse_args().stage
config.init(stage)

with open("./character2.json") as f:
    mockCharacter = json.load(f)

import services.database as database

status, message = database.updateCharacter(mockCharacter)