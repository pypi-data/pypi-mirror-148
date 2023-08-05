import json
import logging
import os
from time import sleep
from bs4 import BeautifulSoup
import requests
import bs4

# import parent dir 
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

URL = "https://honkaiimpact3.fandom.com/wiki/Battlesuits"
BASE_URL= "https://honkaiimpact3.fandom.com"
from honkaiDex.data import HONKAIDEX_DATA

# get script filename
script_name = os.path.basename(__file__).split(".")[0]

data = {}


def parse_base_character(td : bs4.element.Tag):
    # get a
    a = td.find("a")

    href = a.get("href")
    name = a.get("title").strip().lower()

    logging.debug(f"found : {name}")
    dict_data = {
        "link" : href,
    }

    data[name] = dict_data
    return name


def get_bs_rank(main_class : bs4.element.Tag):
    rank_span = main_class.find("span", class_="nomobile")
    rank_img = rank_span.find("img")
    rank = rank_img.get("alt")[0]
    logging.debug(f"rank: {rank}")
    return rank

def get_bs_img(main_class : bs4.element.Tag):
    div = main_class.find("div", class_="stretch-image",
        style="position: relative; max-width: 150px; padding: 1px;"
    )
    img = div.find("img")
    alt = img.get("alt")
    src = img.get("src")
    logging.debug(f"battlesuit: {alt}")
    return alt, src

def get_bs_type(profile_box : bs4.element.Tag):
    # get type
    colors = ["#39d5fd", "#9976ff", "#fd44ac", "#feb22b","#eed390"]

    for color in colors:
        type_span = profile_box.find("span",
            style=f"display: flex; gap: 5px; color: {color};text-align:center;"
        )
        if type_span is not None:
            break

    if type_span is None:
        logging.error(f"not found type")
        return None

    type_span = type_span.find("img")
    return type_span.get("alt")

def get_bs_release_version(profile_box : bs4.element.Tag):
    # get type
    release_div = profile_box.find("div",
        style="border-top: 2px solid rgb(255 255 255 / 20%); line-height: 160%;"
    )

    links = release_div.find_all("a")

    for link in links:
        if link.get("title").startswith("Version"):
            return str(link.get("title").split(" ")[1])

def get_bs_core_strengths(profile_box : bs4.element.Tag):
    attrs = []
    div = profile_box.find("div",
        style="line-height: 160%; padding-right: 5px; margin-left: 10px; margin-right: 10px; padding-bottom: 5px;"
    )
    div = div.find("div",
        style="display: flex; flex-wrap: wrap; gap: 5px;",
    )

    divs = div.find_all("div",
        style="background: white; width: fit-content; border-radius: 5px; box-shadow: inset 0 0 1px 0px #2e85b5; display: flex; align-items: center; padding: 3px; gap: 3px;"
    )
    
    for div in divs:
        div : bs4.element.Tag
        two_divs = div.find_all("div")
        if len(two_divs) != 2:
            logging.error(f"not 2 divs: {two_divs}")
            continue
        tag : bs4.element.Tag = two_divs[1] 
        
        attr = tag.get_text().strip().lower()
        logging.debug(f"find attr: {attr}")
        attrs.append(attr)

    return attrs

def get_battlesuit_data(wiki_address : str):
    battlesuit_page = requests.get(wiki_address)
    battlesuit_soup = BeautifulSoup(battlesuit_page.content, 'html.parser')
    battlesuit_soup.encode("utf-8")

    main_class = battlesuit_soup.find("main", class_="page__main")
    main_class = main_class.find("div", class_="dotted-background",
        style="display: flex; width: fit-content; padding-top: 2px; padding-bottom: 2px; padding-left: 2px; border-radius: 10px; justify-content: flex-start; box-shadow: 0 0 2px rgb(0 0 0 / 50%); margin: 2px; outline: 1px solid rgb(0 0 0 / 20%); background-color: rgb(63 113 152 / 20%);"
    )
    
    rank = get_bs_rank(main_class)
    battlesuit_name, img_src = get_bs_img(main_class)
    
    profile_box = main_class.find("div",
        style="display: flex; flex-direction: column; align-content: flex-start; justify-content: flex-start; align-items: flex-start;"
    )

    bs_type = get_bs_type(profile_box)

    bs_version = get_bs_release_version(profile_box)

    bs_tags = get_bs_core_strengths(profile_box)

    return {
        "name" : battlesuit_name,
        "img" : img_src,
        "type" : bs_type,
        "version" : bs_version,
        "tags" : bs_tags,
        "rank" : rank,
    }


def parse_battlesuit(tr : bs4.element.Tag, name : str):
    # get all a
    battlesuits = []
    a_list = tr.find_all("a")
    for a in a_list:
        href = a.get("href")
        battlesuit_data = get_battlesuit_data(BASE_URL+href)
        battlesuits.append(battlesuit_data)
    return battlesuits

def parse_character(trs, path):

    for tr in trs:
        
        tr : bs4.element.Tag
        first_td : bs4.element.Tag = tr.find("td")
        second_td = first_td.find_next_sibling("td")
        name = parse_base_character(first_td)
        battlsuit_ch = parse_battlesuit(second_td, name)
        data[name] = {
            "name" : name,
            "battlesuit" : battlsuit_ch,
        }
        print()

def parse(path : str):
    page = requests.get(URL)
    #encode utf-8
    sleep(1)
    soup = BeautifulSoup(page.content, 'html.parser')
    soup.encode("utf-8")

    # 
    raw_focus = soup.find(
        "table",
        class_="navbox infobox-base",
        style="width: 100%; vertical-align: left; margin-top: 10px;;"
    )

    raw_focus_1 = raw_focus.find("tr")
    raw_focus_2 = raw_focus_1.find("td")
    raw_focus_3 = raw_focus_2.find("table")

    trs = raw_focus_3.find_all("tr")[1:]
    # remove all tr that has style height:2px;
    selected = []
    for tr in trs:
        if tr.get("style") is not None:
            logging.debug("removing tr with style: %s", tr.get("style"))
            continue
        selected.append(tr)

    del page
    del soup
    del raw_focus
    del raw_focus_1
    del raw_focus_2
    del raw_focus_3

    logging.debug(f"characters: {len(selected)}")
    parse_character(selected, path)

    with open(path, "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

    parse(os.path.join(HONKAIDEX_DATA, f"{script_name}.json"))