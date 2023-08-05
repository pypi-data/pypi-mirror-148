from zxutil.collections import _gconfig, _cconfig

class gconfig(_gconfig):
    MIN_LV = 1
    MAX_LV = 88

    STIGAMATA = "stigamata_1"
    CHARACTER = "character_0"

class config(_cconfig):    
    class data(_cconfig):
        class stigamata_1(_cconfig):
            FILENAME = "stigamata_1.json"

        class character_0(_cconfig):
            FILENAME = "character_0.json"

    class profile(_cconfig):
        class cached(_cconfig):
            STIGAMATA = gconfig
            CHARACTER = gconfig
        class just_stigamata(_cconfig):
            STIGAMATA = gconfig

        class just_character(_cconfig):
            CHARACTER = gconfig
            