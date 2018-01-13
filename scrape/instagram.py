import glob
import json
import os
import requests
import time
import sys
from bs4 import BeautifulSoup
from tqdm import tqdm

INSTAGRAM_URL = 'https://www.instagram.com/'
PHOTOGENIC_DIR = 'photogenic'
PIXEL_SIZE = 640  # 150 240 320 480


def find(dir_name):
    return {os.path.basename(p) for p in
            glob.glob('{}/*.jpg'.format(dir_name))}


def scrape(acc_name, acc_dir, exists):
    acc_url = INSTAGRAM_URL + acc_name
    next_page_url = acc_url

    has_next_page = True
    src_urls = []
    while has_next_page:
        resp = requests.get(next_page_url)
        bs = BeautifulSoup(resp.content, 'html.parser')
        content = bs.body.script.contents[0]
        content_json = content.replace('window._sharedData = ', '')[:-1]
        loaded = json.loads(content_json)
        medias = loaded['entry_data']['ProfilePage'][0]['user']['media']
        nodes = medias['nodes']
        for n in nodes:
            thumnails = n['thumbnail_resources']
            for res in thumnails:
                if res['config_height'] == PIXEL_SIZE:
                    src_urls.append(res['src'])

        # 次のページを取得
        page_info = medias['page_info']
        has_next_page = page_info['has_next_page']
        if has_next_page:
            end_cursor = page_info['end_cursor']
        next_page_url = '{}/?max_id={}'.format(acc_url, end_cursor)
        time.sleep(0.5)

    for src in tqdm(src_urls, ncols=100, ascii=True):
        filename = src.split('/')[-1]
        if filename in exists:
            continue
        filepath = '{}/{}'.format(acc_dir, filename)
        img = requests.get(src)
        with open(filepath, 'wb') as f:
            f.write(img.content)
        time.sleep(1)


FAMOUS_ACCOUNTS = {'lavie_city', 'starbucks_j',
                   'estyle1010', 'keiyamazaki',
                   'feel_kiyomizudera', 'wat.ki',
                   'airio830'}


def main():
    if not os.path.isdir(PHOTOGENIC_DIR):
        os.mkdir(PHOTOGENIC_DIR)
    args = sys.argv
    if len(args) <= 1:
        sys.exit()

    acc_name = args[1:]
    for acc in acc_name:
        acc_dir = '{}/{}'.format(PHOTOGENIC_DIR, acc)
        if not os.path.isdir(acc_dir):
            os.mkdir(acc_dir)
        exists = find(acc_dir)
        scrape(acc, acc_dir, exists)


if __name__ == '__main__':
    main()
