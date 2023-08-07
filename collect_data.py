#!/usr/bin/env python3

import csv
import os
import sys
import requests
from bs4 import BeautifulSoup
import time
from typing import Tuple
import pandas as pd

DATA_DIR = 'data'
DATA_FILE = DATA_DIR + '/raw_data.csv'

CSV_LABEL = []
HORSE_TOTAL = 18

START_YEAR = 2020
END_YEAR = 2022

def initialize():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.isfile(DATA_FILE):
        csv_label = ['race_id', 'class', 'distance', 'weather', 'condition']
        for i in range(HORSE_TOTAL):
            csv_label.append(f'waku{i}')
            csv_label.append(f'umaban{i}')
            csv_label.append(f'uma_id{i}')
            csv_label.append(f'sex{i}')
            csv_label.append(f'barei{i}')
            csv_label.append(f'sekiryo{i}')
            csv_label.append(f'kisyu_id{i}')
            csv_label.append(f'bataiju{i}')
            csv_label.append(f'zogen{i}')
        csv_label.append('rank1')
        csv_label.append('rank2')
        csv_label.append('rank3')

        with open(DATA_FILE, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(csv_label)

        return None

    else:
        df = pd.read_csv(DATA_FILE)

        return df


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


def parse_horse_sex_barei(horse_info: str) -> Tuple[int, int]:
    tmp = horse_info

    if '牝' in tmp:
        sex = 0
        tmp = tmp.replace('牝', '')
    elif '牡' in tmp:
        sex = 1
        tmp = tmp.replace('牡', '')
    elif 'セ' in tmp:
        sex = 2
        tmp = tmp.replace('セ', '')
    else:
        print(f'horse sex error: {tmp}')
        sys.exit(1)

    return int(sex), int(tmp)


def main():
    df = initialize()

    exist_race_id = []
    if df is not None:
        exist_race_id = df['race_id'].tolist()

    print(exist_race_id)

    for year in range(START_YEAR, END_YEAR + 1):
        for place in range(1, 11):
            for kaisai in range(1, 7):
                for kaisai_day in range(1, 13):
                    for race_num in range(1, 13):

                        race_id = str(year) + str(place).zfill(2) + str(kaisai).zfill(2) + \
                                  str(kaisai_day).zfill(2) + str(race_num).zfill(2)

                        if int(race_id) in exist_race_id:
                            continue

                        req_url = SHUTSUBA_URL + race_id

                        print(req_url)

                        try:
                            req = requests.get(req_url)
                        except requests.exceptions.RequestException as e:
                            print(f'error: {e}')
                            time.sleep(10)
                            req = requests.get(req_url)
                        time.sleep(1)

                        soup = BeautifulSoup(req.content.decode('euc-jp', 'ignore'), 'html.parser')

                        uma_list = soup.find_all(class_='HorseList')

                        if len(uma_list) == 0:
                            continue

                        # race info
                        race_info = soup.find(class_='RaceList_Item02')

                        race_class_sub = str(race_info.find(class_='RaceData01').find_all('span')[0])
                        race_class, race_distance = parse_race_class(race_class_sub)

                        race_weather_sub = str(race_info.find(class_='RaceData01').find_all('span')[1])
                        race_weather = parse_race_weather(race_weather_sub)

                        race_condition_sub = str(race_info.find(class_='RaceData01').find_all('span')[2])
                        race_condition = parse_race_condition(race_condition_sub)

                        shusso = len(uma_list)

                        tmp_horse_list = []
                        for i in range(HORSE_TOTAL):
                            waku = -1
                            umaban = -1
                            uma_id = -1
                            sex = -1
                            barei = -1
                            sekiryo = -1
                            kisyu_id = -1
                            bataiju = -1
                            zogen = -1

                            if i >= (shusso - 1):
                                tmp_horse_list.append([waku, umaban, uma_id, sex, barei, sekiryo, kisyu_id, bataiju, zogen])
                                continue

                            uma_info = uma_list[i]

                            if uma_info.find(class_='Cancel_Txt') is not None:
                                tmp_horse_list.append([waku, umaban, uma_id, sex, barei, sekiryo, kisyu_id, bataiju, zogen])
                                continue

                            waku = int(str(uma_info.find_all(class_='Txt_C')[0]).split('>')[2].split('<')[0])
                            umaban = int(str(uma_info.find_all(class_='Txt_C')[1]).split('>')[1].split('<')[0])
                            uma_id = int(str(uma_info.find(class_='HorseName').find('a')).split()[7].split('_')[1].replace('"', ''))
                            tmp = str(uma_info.find(class_='Barei')).split('>')[1].split('<')[0]
                            sex, barei = parse_horse_sex_barei(tmp)
                            sekiryo = float(str(uma_info.find_all(class_='Txt_C')[3]).split('>')[1].split('<')[0])
                            kisyu_id = int(str(uma_info.find(class_='Jockey').find('a')).split('"')[1].split('/')[6])
                            bataiju = int(str(uma_info.find(class_='Weight')).split('>')[1].split('<')[0].replace('\n', ''))
                            zogen = int(str(uma_info.find(class_='Weight')).split('(')[1].split(')')[0])

                            tmp_horse_list.append([waku, umaban, uma_id, sex, barei, sekiryo, kisyu_id, bataiju, zogen])

                        req_url = RESULT_URL + race_id

                        print(req_url)

                        try:
                            req = requests.get(req_url)
                        except requests.exceptions.RequestException as e:
                            print(f'error: {e}')
                            time.sleep(10)
                            req = requests.get(req_url)
                        time.sleep(1)

                        soup = BeautifulSoup(req.content.decode('euc-jp', 'ignore'), 'html.parser')

                        rank_list = soup.find_all(class_='HorseList')
                        rank_info = rank_list[0]
                        rank_1 = int(str(rank_info.find_all(class_='Txt_C')[0]).split('>')[2].split('<')[0])
                        rank_info = rank_list[1]
                        rank_2 = int(str(rank_info.find_all(class_='Txt_C')[0]).split('>')[2].split('<')[0])
                        rank_info = rank_list[2]
                        rank_3 = int(str(rank_info.find_all(class_='Txt_C')[0]).split('>')[2].split('<')[0])

                        tmp_race_data = [[race_id, race_class, race_distance, race_weather, race_condition], sum(tmp_horse_list, []), [rank_1, rank_2, rank_3]]
                        print(sum(tmp_race_data, []))

                        with open(DATA_FILE, 'a') as f:
                            writer = csv.writer(f)
                            writer.writerow(sum(tmp_race_data, []))

if __name__ == '__main__':
    main()
