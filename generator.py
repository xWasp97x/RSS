from rfeed import *

output_file = '/mnt/nas/rss/torrent_rss.xml'
input_file = '/mnt/nas/rss/magnets.txt'


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

with open(output_file, 'w') as file:
    file.write(rss)
