import logging
import os
import json

HONKAIDEX_DATA = os.path.dirname(os.path.realpath(__file__))

__LOADED_TRACK__ = {}

def load_once():
    # wrapper
    def load_once_wrapper(func):
        def wrapper(*args, **kwargs):
            func_module = str(func.__module__)

            if func_module+func.__name__ in __LOADED_TRACK__:
                # get func module name

                logging.debug(f"{func_module}.{func.__name__} already loaded")
                return
            __LOADED_TRACK__[func_module+func.__name__] = True
            logging.debug(f"{func_module}.{func.__name__} loaded")
            return func(*args, **kwargs)
        return wrapper

    return load_once_wrapper

# load function
def load(load_str : str):
    # based on str find .py file within package
    # load_str = "honkaiDex.data.stigamata.stigamata_1"
    import importlib
    logging.debug(f"loading module {load_str}")
    mod = importlib.import_module("honkaiDex.data."+load_str)
    if not hasattr(mod, "load"):
        logging.debug(f"{load_str} has no load function")

    mod.load()
