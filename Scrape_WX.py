"""

This script scrapes one day of weather station data
from a personal weather station

@author: Benjamin Clouser

"""
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import argparse

def helper(dct):
    try:
        return len(dct['observations'])
    except:
        return 0

parser = argparse.ArgumentParser('Scrapes one day of weather station data and writes to csv.')
parser.add_argument('-s', '--station_id', default='KILCHICA854', help='Wunderground Personal Weather Station ID')
parser.add_argument('-y', '--year', default=2023, help='Year')
parser.add_argument('-m', '--month', default=1, help='Month')
parser.add_argument('-d', '--day', default=1, help='Day')
args = parser.parse_args()

station_id = args.station_id
year = f"{int(args.year):04d}"
mo = f"{int(args.month):02d}"
dy = f"{int(args.day):02d}"

date=year + '-' + mo + '-' + dy

url = 'https://www.wunderground.com/dashboard/pws/' + station_id + '/table/' + date +'/' + date +'/daily'

response = requests.get(url)

soup = BeautifulSoup(response.text,features='lxml')
pws_raw = soup.select('script#app-root-state')

pws_txt = str(pws_raw[0].text).replace('&q;','"')
pws_dict = json.loads(pws_txt)

keys = list(pws_dict['wu-next-state-key'])

entry_lengths = [helper((((pws_dict['wu-next-state-key'])[x])['value'])) for x in keys]

obs_index = entry_lengths.index(max(entry_lengths))

df = pd.json_normalize((((pws_dict['wu-next-state-key'])[keys[obs_index]])['value'])['observations'],sep='_')

df.to_csv(station_id + '_' + date + '.csv')


