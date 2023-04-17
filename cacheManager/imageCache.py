import redis

import configparser
config = configparser.ConfigParser()
config.read('config.ini')


"""
    TODO:
        - Make sure that inserts goes in order
"""


class imageCacheManager:
    def __init__(self):
        self.pool = redis.ConnectionPool(host=config["redis"]["host"], port=int(config["redis"]["port"]), db=config["redis"]["database"], password=config["redis"]["password"])
        self.redis = redis.Redis(connection_pool=self.pool)

    def cacheImage(self, answer: int, imageDataBase64: str) -> bool:
        self.redis.set(answer, imageDataBase64)

        return True


    def getImageFromCache(self) -> (str, str):
        keysFetch = []
        for key in self.redis.scan_iter("*"):
            keysFetch.append(key.decode("utf-8"))
        key = keysFetch[-1:][0]

        """
        First we iterate through redis keys and then put them into list and decode them as UTF-8
        because default redis output is bytes, then we first put them into keysFetch temporary list
        and do keysFetch[-1:] to get FIFO instead of LIFO because by default redis will return
        keys from top of the list and we do not want that because that way we would repeat same captcha
        over and over and we want to avoid that.
        EXAMPLE:
            keysFetch = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
            10 is the latest captcha we cached
            we call keys = keysFetch[-1:] and we get 1 (FIFO).
        """

        output = (key, self.redis.get(key).decode("utf-8"))

        self.redis.delete(key)

        return output
