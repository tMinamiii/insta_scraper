import json
import os
import requests
import time
from bs4 import BeautifulSoup

INSTAGRAM_URL = 'https://www.instagram.com/'
FAMOUS_ACCOUNTS = {'lavie_city', 'starbucks_j',
                   'estyle1010', 'feel_kiyomizudera'}
PHOTOGENIC_DIR = 'photogenic'


def scrape(acc_name):
    if not os.path.isdir(PHOTOGENIC_DIR):
        os.mkdir(PHOTOGENIC_DIR)

    acc_url = INSTAGRAM_URL + acc_name
    next_page_url = acc_url

    has_next_page = True
    while has_next_page:
        resp = requests.get(next_page_url)
        bs = BeautifulSoup(resp.content, 'html.parser')
        content = bs.body.script.contents[0]
        content_json = content.replace('window._sharedData = ', '')[:-1]
        loaded = json.loads(content_json)
        medias = loaded['entry_data']['ProfilePage'][0]['user']['media']
        nodes = medias['nodes']
        for n in nodes:
            for res in n['thumbnail_resources']:
                if res['config_height'] == 640:
                    photo_url = res['src']
                    filename = photo_url.split('/')[-1]
                    filepath = '{}/{}'.format(PHOTOGENIC_DIR, filename)
                    photo = requests.get(photo_url)
                    with open(filepath, 'wb') as f:
                        f.write(photo.content)
                    time.sleep(1)
        # 次のページを取得
        page_info = medias['page_info']
        has_next_page = page_info['has_next_page']
        if has_next_page:
            end_cursor = page_info['end_cursor']
            next_page_url = '{}/?max_id={}'.format(acc_url, end_cursor)


scrape('lavie_city')
