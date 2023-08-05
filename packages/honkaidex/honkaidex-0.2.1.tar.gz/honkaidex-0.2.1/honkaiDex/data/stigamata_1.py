from honkaiDex.base.stigamata import StigamataSet
import logging
import json
from honkaiDex.data import HONKAIDEX_DATA, load_once
from honkaiDex import config
import os 

@load_once()
def load():

    logging.debug(f"Loading {config.data.stigamata_1.FILENAME}")

    json_data = {}

    with open(os.path.join(HONKAIDEX_DATA, config.data.stigamata_1.FILENAME), "r") as f:
        json_data = json.load(f)

    StigamataSet.from_json(data=json_data)
    