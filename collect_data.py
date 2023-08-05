#!/usr/bin/env python3

import os
import sys
import requests
from bs4 import BeautifulSoup
import time
from typing import Tuple

DATA_DIR = 'data'
DATA_FILE = DATA_DIR + '/raw_data.csv'

SHUTSUBA_URL = ''
RESULT_URL = ''

def initialize():
    os.makedirs(DATA_DIR, exist_ok=True)

def parse_race_class(race_class: str) -> Tuple[int, int]:
    tmp = race_class.replace('<span>', '').replace(' ', '').replace('</span>', '')

    if '芝' in tmp:
        race_class = 0
        tmp = tmp.replace('芝', '')
    elif 'ダ' in tmp:
        race_class = 1
        tmp = tmp.replace('ダ', '')
    elif '障' in tmp:
        race_class = 2
        tmp = tmp.replace('障', '')
    else:
        print(f'tmp error: {tmp}')
        sys.exit(1)

    tmp = tmp.replace('m', '')

    return race_class, int(tmp)

def parse_race_weather(race_weather: str) -> int:
    tmp = race_weather.replace('<span>', '').replace('</span>', '')
    tmp = tmp.replace('<span class="Icon_Weather', '').replace(' ', '').replace('">', '')
    tmp = tmp.replace('Weather', '')

    return int(tmp)

def parse_race_condition(race_condition: str) -> int:
    tmp = race_condition.split()[2].replace('</span>', '').split(':')[1]

    if '良' in tmp:
        ret = 0
    elif '稍' in tmp:
        ret = 1
    elif '重' in tmp:
        ret = 2
    elif '不' in tmp:
        ret = 3
    else:
        print(f'race condition error: {tmp}')
        sys.exit(1)

    return int(ret)

def main():
    initialize()

    race_id = str(year) + str(place).zfill(2) + str(kaisai).zfill(2) + \
              str(kaisai_day).zfill(2) + str(race_num).zfill(2)

    req_url = SHUTSUBA_URL + race_id

    print(req_url)

    try:
        req = requests.get(req_url)
    except requests.exceptions.RequestException as e:
        print(f'error: {e}')
        time.sleep(10)
        req = requests.get(req_url)

    soup = BeautifulSoup(req.content.decode('euc-jp', 'ignore'), 'html.parser')

    uma_list = soup.find_all(class_='HorseList')

    # race info
    race_info = soup.find(class_='RaceList_Item02')
    print(race_info.find(class_='RaceData01').find_all('span'))

    race_class_sub = str(race_info.find(class_='RaceData01').find_all('span')[0])
    print(parse_race_class(race_class_sub))
    race_class, race_distance = parse_race_class(race_class_sub)

    race_weather_sub = str(race_info.find(class_='RaceData01').find_all('span')[1])
    print(parse_race_weather(race_weather_sub))
    race_weather = parse_race_weather(race_weather_sub)

    race_condition_sub = str(race_info.find(class_='RaceData01').find_all('span')[2])
    print(parse_race_condition(race_condition_sub))
    race_condition = parse_race_condition(race_condition_sub)


if __name__ == '__main__':
    main()
