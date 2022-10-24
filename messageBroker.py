from time import sleep

import redis as redis
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SubPub:
    red = redis.StrictRedis('redis', 6379, charset="utf-8", decode_responses=True)

    def perform(self, sub_chanel, pub_chanel, func):
        p = self.red.pubsub()
        p.subscribe(sub_chanel)

        while True:
            message = p.get_message()
            if not message:
                sleep(2)
                continue

            if message["type"] == "subscribe":
                continue

            logger.info(f"Executing search password result after receiving message: {message}")
            result = func()
            logger.info(f"result: {result}")
            self.red.publish(pub_chanel, result)
            break
        self.red.close()
