from rfeed import *
from time import sleep
import os
from loguru import logger
from threading import Thread

PORT = 8080

output_file = '/RSS/output/rss.xml'

input_file = '/RSS/input/magnets.txt'

log_format = '<light-black>{time:YYYY-MM-DD HH:mm:ss.SSS}</light-black>' \
             ' <level>{name}.{function}@{line} | {level}: {message}</level>'

logs_path = '/RSS/logs'


def init_logger():
    logger.remove()
    logger.add(sys.stdout, format=log_format, colorize=True)
    logger.add(os.path.join(logs_path, '{time:YYYY-MM-DD}.log'), format=log_format,
               colorize=False, compression='zip', rotation='00:00')


@logger.catch
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
    init_logger()

    logger.info('Launching http server')

    Thread(target=os.system, args=(f'cd /RSS/output/; python3 -m http.server {PORT}',)).start()

    while True:
        logger.info('Generating new rss...')
        generate_rss()
        logger.success('New rss generated.')
        sleep(60)
