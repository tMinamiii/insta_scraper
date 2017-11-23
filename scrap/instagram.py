import json
import os
import requests
from bs4 import BeautifulSoup

INSTAGRAM_URL = 'https://www.instagram.com/'
FAMOUS_ACCOUNTS = {'lavie_city', 'starbucks_j',
                   'estyle1010', 'feel_kiyomizudera'}
PHOTOGENIC_DIR = 'photogenic'


def scrape(self):
    if not os.path.isdir(PHOTOGENIC_DIR):
        os.mkdir(PHOTOGENIC_DIR)

    for acc_name in FAMOUS_ACCOUNTS:
        acc_url = INSTAGRAM_URL + acc_name
        resp = requests.get(acc_url)
        bs = BeautifulSoup(resp.content, 'html.parser')
        content = bs.body.script.contents[0]
        content_json = content.replace('window._sharedData = ', '')[:-1]
        loaded = json.loads(content_json)
        medias = loaded['entry_data']['ProfilePage'][0]['user']['media']
        for res in [m['thumbnail_resources'] for m in medias]:
            if res['content_heigh'] == 640:
                photo_url = res['src']
                filename = photo_url.split('/')[-1]
                filepath = '{}/{}'.format(PHOTOGENIC_DIR, filename)
                photo = requests.get(photo_url)
                with open(filepath, 'wb') as f:
                    f.write(photo)
