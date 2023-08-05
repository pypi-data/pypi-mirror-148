from honkaiDex.base.character import BaseCharacter, Battlesuit
import logging
import json
from honkaiDex.data import HONKAIDEX_DATA, load_once
from honkaiDex import config
import os 

@load_once()
def load():

    logging.debug(f"Loading {config.data.character_0.FILENAME}")

    json_data :dict = {}

    with open(os.path.join(HONKAIDEX_DATA, config.data.character_0.FILENAME), "r") as f:
        json_data = json.load(f)

    for character_data in json_data.values():
        character_data : dict
        character = BaseCharacter.create(
            name=character_data["name"],
            nickname=character_data.get("nickname", []),
        )


        for bs_data in character_data.get("battlesuit", []):
            bs_data : dict
            bs = Battlesuit.create(
                base_character=character,
                name=bs_data["name"],
                type=bs_data["type"],
                version_released=bs_data["version"],
                rarity=bs_data["rank"],
                tags=bs_data.get("tags", []),
                img_link=bs_data.get("img", None),
                nickname=bs_data["nickname"]
            )
