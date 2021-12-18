from rfeed import *
import wget
from time import sleep
import os

PORT = 6969

output_file = './output/torrent_rss.xml'

with open('./config/magnets_file_link') as file:
    input_file = file.read().strip()


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

    if os.path.exists('./magnets.txt'):
        os.remove('./magnets.txt')

    wget.download(input_file, './magnets.txt')

    with open('./magnets.txt') as file:
        items = [get_item(magnet) for magnet in file.readlines()]

    feed = Feed(title='Torrents feed',
                language='en-US',
                description='desc',
                link='google.it',
                items=items)

    rss = feed.rss()

    with open(output_file, 'w') as file:
        file.write(rss)


if __name__ == '__main__':

    os.system(f'cd ./output; python3 -m http.server {PORT}')

    while True:
        generate_rss()
        sleep(60 * 5)
