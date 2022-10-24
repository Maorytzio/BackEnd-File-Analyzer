import glob
import json
import logging
import os
from time import sleep

import redis

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def file_analyzer():

    dir_name = os.path.abspath("theHarvester")
    list_of_files = list(filter(os.path.isfile,
                                glob.glob(dir_name + '/**/*', recursive=True)))

    list_of_files = sorted(list_of_files,
                           key=lambda x: os.stat(x).st_size, reverse=True)

    files_count_dict = get_file_count_dic(list_of_files)

    top_10_files_size = {
        file_name: os.stat(file_name).st_size
        for file_name in list_of_files[:10]
    }

    return {
        "top_10_files": top_10_files_size,
        "file_types": {k: v for k, v in files_count_dict.items() if k != ""}
    }


def get_file_count_dic(list_of_files):
    files_dic = {}

    for file_name in list_of_files:
        base_name = os.path.basename(file_name)
        ext = os.path.splitext(base_name)[1]
        if files_dic.get(ext) is None:
            files_dic.setdefault(ext, 1)
        else:
            files_dic[ext] += 1

    return files_dic


def subscribe_and_analyze():

    red = redis.StrictRedis('redis', 6379, charset="utf-8", decode_responses=True)
    p = red.pubsub()
    p.subscribe('get-top-10-files')

    while True:
        message = p.get_message()
        if not message:
            sleep(2)
            continue

        if message["type"] == "subscribe":
            continue

        logger.info(f"Executing analyze result after receiving message: {message}")
        result = file_analyzer()
        logger.info(f"result: {result}")
        red.publish("get-top-10-files-result", json.dumps(result))
        break
    red.close()


if __name__ == '__main__':
    logger.info("Analyze module is listening...")
    subscribe_and_analyze()
