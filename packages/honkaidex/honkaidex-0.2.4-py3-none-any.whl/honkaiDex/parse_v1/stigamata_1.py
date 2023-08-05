import json
import logging
import os
from time import sleep
from bs4 import BeautifulSoup
import requests

# import parent dir 
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

BASE_URL = "https://honkaiimpact3.fandom.com"
URL = "https://honkaiimpact3.fandom.com/wiki/Stigmata"


from honkaiDex.data import HONKAIDEX_DATA

# get script filename
script_name = os.path.basename(__file__).split(".")[0]

data = []

def parse_stig_page(href : str, name : str, top_img=None, mid_img =None, bot_img =None):
    page = requests.get(BASE_URL + href)
    soup = BeautifulSoup(page.content, 'html.parser')

    # 
    entry = {}

    # 
    if "(" in name:
        name = name.split("(")[0]
    entry["name"] = name

    # get effects div
    base_effects_div = soup.find("div" ,id="mw-content-text")
    
    effect_divs = base_effects_div.find_all("div", style="width: fit-content; max-width: 600px; padding: 5px; display: flex; flex-direction: column; margin: 2px; box-shadow: 0 0 2px rgb(0 0 0 / 50%); border-radius: 5px;")
    for i, effect in enumerate(effect_divs):
        # get 2nd div in effect div
        effect_div = effect.find_all("div")[1]
        # get str
        effect_str = effect_div.get_text()
        
        if i == 0:
            entry["top_e"] = effect_str
        elif i == 1:
            entry["mid_e"] = effect_str
        elif i == 2:
            entry["bot_e"] = effect_str
    
    binded_effects_div = base_effects_div.find("div", style="display: flex; flex-wrap: wrap; gap: 10px;", class_="cflex-nowrap")
    binded_effects_div = binded_effects_div.find("div", style="display: flex; flex-direction: column;")
    binded_effects_divs = binded_effects_div.find_all("div")
    for i, binded_effect in enumerate(binded_effects_divs):
        if i == 1:
            entry["two_piece"] = binded_effect.get_text()
        elif i == 3:
            entry["three_piece"] = binded_effect.get_text()
    
    # image
    if top_img is not None:
        entry["top_img"] = top_img

    if mid_img is not None:
        entry["mid_img"] = mid_img
    
    if bot_img is not None:
        entry["bot_img"] = bot_img

    # get obtainable from data
    try:
        obtainable_div = base_effects_div.find("div", style="min-width: fit-content; width: fit-content; padding: 5px; display: flex; flex-direction: column; gap: 5px; margin: 2px; box-shadow: 0 0 2px rgb(0 0 0 / 50%); border-radius: 5px;", class_="infobox-base")
        # find all divs inside
        obtainable_divs = obtainable_div.find_all("div")
        entry["obtainable"] = []
        for i, odive in enumerate(obtainable_divs):
            if i == 0:
                continue
            # get text
            
            obtainable_str = odive.get_text()
            if "❌" in obtainable_str:
                continue

            obtainable_str = obtainable_str[2:]
            entry["obtainable"].append(obtainable_str)
    except:
        pass
    
    global data
    data.append(entry)

def parse(path:str):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    # get div main-container 
    main_container = soup.find("div", {"class" : "main-container"})

    parent_div = main_container.find("div", {"style" : "display: flex; flex-wrap: wrap; gap: 5px;"})

    # get all divs
    divs = parent_div.find_all("div", style="border-radius: 10px; padding: 2px; background-color: rgb(55 87 126 / 20%); border: 1px solid #2E85B5; width: min-content; display: flex; word-break: break-word; text-align: center; font-size: 13px; flex-direction: column;")

    for div in divs:
        stig_meta = div.find_all("a")
        stig_div = stig_meta[0]

        alt_image = stig_div.find("img")
        print(f"found {stig_div.get('href')}")
        logging.debug(alt_image['data-src'])

        parse_stig_page(
            href=stig_div.get('href'),
            name= stig_div.get('title'),  
            top_img=alt_image['data-src'], 
            mid_img=stig_meta[1].find("img")['data-src'],
            bot_img=stig_meta[2].find("img")['data-src'],
        )
        sleep(1)

    # write to file
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

if __name__ == '__main__':
    parse(os.path.join(HONKAIDEX_DATA, f"{script_name}.json"))