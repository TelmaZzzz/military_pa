import json
from bs4 import BeautifulSoup as BS 
import requests
import logging
import time
import pandas as pd
from functools import wraps


PREFIX = "https://en.wikipedia.org"
logging.getLogger().setLevel(logging.INFO)
requests.adapters.DEFAULT_RETRIES = 5
ARR_name = []
ARR_text = []
ARR_country = []
ARR_url = []

def error_wrapper(func):
    try:
        func()
    except Exception as e:
        logging.warning(e)
    return func

def wikipedia_pa(url):
    while True:
        try:
            req = requests.get(url=url).text
            return BS(req, 'html.parser')
        except Exception as e:
            logging.info('error_msg is:{} try url:{} again in 1s.'.format(e, url))
            time.sleep(1)

def get_text(url):
    html = wikipedia_pa(url)
    context_div = html.find("div", class_="mw-parser-output")
    text = ""
    for iter in list(context_div):
        if iter.name == "p":
            for line in list(iter):
                try:
                    text += line.text
                except:
                    text += line.string
    return text

def get_country(name):
    st = None
    en = None
    for inx, ch in enumerate(name):
        if ch == "(":
            st = inx
        elif ch == ")":
            en = inx
    if st and en:
        return name[st+1:en]
    else:
        return "NULL"

def change_name(name):
    st = None
    en = None
    for inx, ch in enumerate(name):
        if ch == "(":
            st = inx
        elif ch == ")":
            en = inx
    if st and en:
        return name[:st]
    else:
        return name

# @error_wrapper
def gen_country_weapons(url):
    html = wikipedia_pa(url)
    context_div = html.find("div", class_="mw-parser-output")
    context_div = list(context_div)
    country = None
    for iter in context_div:
        if iter.name == "h2":
            country = iter.find("span", class_="mw-headline").text
            if country == "See also":
                break
        if iter.name == "ul":
            li_list = iter.find_all("li")
            for li in li_list:
                try:
                    href = li.a['href']
                    if href.startswith("/wiki"):
                        # print(PREFIX + href)
                        text = get_text(PREFIX + href)
                    else:
                        continue
                except:
                    continue
                ARR_name.append(li.text)
                ARR_text.append(text)
                ARR_country.append(country)
                ARR_url.append(PREFIX + href)
                print(li.text)
                # ARR.append({
                #     "name":li.text,
                #     "text":text,
                #     "country":country,
                #     "url":PREFIX + href
                # })
    logging.info("Task finished... url is :{}".format(url))

# @error_wrapper
def gen_ul_weapons(url, start_ul):
    html = wikipedia_pa(url)
    context_div = html.find("div", class_="mw-parser-output")
    ul_list = context_div.find_all("ul")
    ul_list[start_ul:]
    for iter in ul_list:
        li_list = iter.find_all("li")
        for li in li_list:
            try:
                href = li.a["href"]
                if href.startswith("/wiki"):
                    text = get_text(PREFIX + href)
                else:
                    continue
            except:
                continue
            ARR_name.append(change_name(li.text))
            ARR_text.append(text)
            ARR_country.append(get_country(li.text))
            ARR_url.append(PREFIX + href)
            # ARR.append({
            #     "name":change_name(li.text),
            #     "text":text,
            #     "country":get_country(li.text),
            #     "url":PREFIX + href
            # })
    logging.info("Task finished... url is :{}".format(url))

# @error_wrapper
def gen_tabel_wwapons(url, name_index, country_index):
    html = wikipedia_pa(url)
    context_div = html.find("div", class_="mw-parser-output")
    table_list = context_div.find_all("table")
    for iter in table_list:
        tbody_list = iter.find("tbody")
        tr_list = tbody_list.find_all("tr")
        for tr in tr_list:
            td_list = tr.find_all("td")
            try:
                href = td_list[name_index].find("a")["href"]
                if href.startswith("/wiki"):
                    text = get_text(PREFIX + href)
                else:
                    continue
            except:
                continue
            ARR_name.append(td_list[name_index].text)
            ARR_text.append(text)
            ARR_country.append(str(td_list[country_index].text).strip())
            ARR_url.append(PREFIX + href)
            # ARR.append({
            #     "name":td_list[name_index].text,
            #     "text":text,
            #     "country":str(td_list[country_index].text).strip(),
            #     "url":PREFIX + href
            # })
    logging.info("Task finished... url is :{}".format(url))

if __name__ == '__main__':
    gen_country_weapons("https://en.wikipedia.org/wiki/List_of_anti-aircraft_weapons")
    gen_country_weapons("https://en.wikipedia.org/wiki/List_of_orbital_launch_systems")
    gen_country_weapons("https://en.wikipedia.org/wiki/List_of_sounding_rockets")
    gen_country_weapons("https://en.wikipedia.org/wiki/List_of_modern_armoured_fighting_vehicles")
    gen_ul_weapons("https://en.wikipedia.org/wiki/List_of_aircraft_weapons", 0)
    gen_ul_weapons("https://en.wikipedia.org/wiki/List_of_missiles", 1)
    gen_tabel_wwapons("https://en.wikipedia.org/wiki/List_of_flamethrowers", 0, 2)
    gen_tabel_wwapons("https://en.wikipedia.org/wiki/List_of_bullpup_firearms", 0, 4)
    gen_tabel_wwapons("https://en.wikipedia.org/wiki/List_of_assault_rifles", 0, 4)
    gen_tabel_wwapons("https://en.wikipedia.org/wiki/List_of_battle_rifles", 0, 4)
    gen_tabel_wwapons("https://en.wikipedia.org/wiki/List_of_multiple-barrel_firearms", 0, 4)
    gen_tabel_wwapons("https://en.wikipedia.org/wiki/List_of_pistols", 0, 4)
    gen_tabel_wwapons("https://en.wikipedia.org/wiki/List_of_revolvers", 0, 4)
    gen_tabel_wwapons("https://en.wikipedia.org/wiki/List_of_submachine_guns", 0, 4)
    gen_tabel_wwapons("https://en.wikipedia.org/wiki/List_of_carbines", 0, 4)
    gen_tabel_wwapons("https://en.wikipedia.org/wiki/List_of_shotguns", 0, 4)
    gen_tabel_wwapons("https://en.wikipedia.org/wiki/List_of_bolt_action_rifles", 0, 4)
    gen_tabel_wwapons("https://en.wikipedia.org/wiki/List_of_sniper_rifles", 0, 4)
    gen_tabel_wwapons("https://en.wikipedia.org/wiki/List_of_machine_guns", 0, 4)
    gen_tabel_wwapons("https://en.wikipedia.org/wiki/List_of_recoilless_rifles", 0, 4)
    gen_tabel_wwapons("https://en.wikipedia.org/wiki/List_of_grenade_launchers", 0, 4)
    gen_tabel_wwapons("https://en.wikipedia.org/wiki/List_of_rocket_launchers", 0, 4)
    gen_tabel_wwapons("https://en.wikipedia.org/wiki/List_of_blow-forward_firearms", 0, 4)
    gen_tabel_wwapons("https://en.wikipedia.org/wiki/List_of_delayed-blowback_firearms", 0, 4)
    gen_tabel_wwapons("https://en.wikipedia.org/wiki/List_of_military_rockets", 0, 2)
    dataframe = pd.Dataframe({
        "name":ARR_name,
        "text":ARR_text,
        "country":ARR_country,
        "url":ARR_url
    })
    dataframe.to_csv("gen.csv", sep=",")

    # print(get_text("https://en.wikipedia.org/wiki/Air_Defense_Anti-Tank_System"))
    # print(get_text("https://en.wikipedia.org/wiki/RBS_70"))
    
