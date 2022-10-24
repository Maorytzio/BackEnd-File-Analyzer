import json
import logging
from time import sleep

import redis

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

red = redis.StrictRedis('redis', 6379, charset="utf-8", decode_responses=True)


def search_password():
    red.publish("search-password", "1")
    p = red.pubsub()
    p.subscribe('search-password-result')

    while True:
        logger.info("Waiting for response from the search password module...")
        message = p.get_message()
        if not message:
            sleep(2)
            continue
        elif message["type"] == "subscribe":
            logger.info(f"Message Check: {message}")
            continue
        else:
            break
    logger.info(f"Returning result: {message}")
    return message["data"]


def get_top_10_files():
    red.publish("get-top-10-files", "1")
    p = red.pubsub()
    p.subscribe('get-top-10-files-result')

    while True:
        logger.info("Waiting for response from the search analyze module...")
        message = p.get_message()
        if not message:
            sleep(2)
            continue
        elif message["type"] == "subscribe":
            continue
        else:
            break
    logger.info(f"Returning result: {message}")
    return message["data"]


if __name__ == '__main__':

    sleep(5)
    logger.info("Controller module is running and listening...")

    analyze_result = get_top_10_files()
    password_result = search_password()

    with open("/output/result.json", 'w') as f:
        f.write(json.dumps({
            "analyze_result": analyze_result,
            "password_result": password_result
        }, indent=4))

    red.close()
