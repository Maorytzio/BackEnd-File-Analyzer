import glob
import os
import logging
from messageBroker import SubPub

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PASSWORD_TXT = b'password'


def perform() -> bytes:
    dir_name = os.path.abspath("theHarvester")

    list_of_files = filter(os.path.isfile,
                           glob.glob(dir_name + '/**/*', recursive=True))

    for file in list_of_files:
        with open(file, 'rb') as f:
            for line in f.readlines():
                words = line.split(b" ")
                for i, w in enumerate(words):
                    if PASSWORD_TXT in w:
                        return words[i + 1]  # The password is a string: ["Paswword:","canufindthis"]

    return b"no-data"


if __name__ == '__main__':
    logger.info("Password module is listening...")
    pub_sub = SubPub()
    pub_sub.perform('search-password', "search-password-result", perform)
