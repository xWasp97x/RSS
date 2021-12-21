from rfeed import *
import wget
from time import sleep
import os
from loguru import logger

PORT = 8080

output_file = '/RSS/output/torrent_rss.xml'

input_file = '/RSS/input/magnets.txt'


def generate_rss():
    def get_item(magnet: str):
        return Item(title=get_name(magnet),
                    link=magnet,
                    description='',
                    author='Script')

    def get_name(magnet: str) -> str:
        start = magnet.index('&dn')
        end = magnet.index('&tr')
        return magnet[start + 4:end].replace('%20', ' ')

    with open(input_file) as file:
        items = [get_item(magnet) for magnet in file.readlines()]

    feed = Feed(title='Torrents feed',
                language='en-US',
                description='desc',
                link='google.it',
                items=items)

    rss = feed.rss()

    logger.info(f'Writing  {output_file}')
    with open(output_file, 'w') as file:
        file.write(rss)


if __name__ == '__main__':

    os.system(f'cd /RSS/output/; python3 -m http.server {PORT}')

    while True:
        logger.info('Generating new rss...')
        generate_rss()
        logger.success('New rss generated.')
        sleep(60 * 5)
