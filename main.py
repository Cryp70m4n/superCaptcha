#!/usr/bin/env python3

from flask import Flask, request
import json
import binascii
import os

import configparser
config = configparser.ConfigParser()
config.read('config.ini')

from cachetools import TTLCache

cache = TTLCache(maxsize=10, ttl=int(config['captcha']['expiry'])*60)


from captchaGenerator.imageGenerator import generateCaptcha
from cacheManager.imageCache import imageCacheManager


captchaGenerator = generateCaptcha()

cacheManager = imageCacheManager()


host = config['web']['host']
port = int(config['web']['port'])


app = Flask(__name__)


requestCounter = 0



@app.route("/captcha/generate", methods=['POST'])
def generate():
    global requestCounter
    if requestCounter >= int(config['captcha']['useCache']):
        gen = cacheManager.getImageFromCache()
        img = gen[1]
        answer = gen[0]

        requestCounter = -1

    else:
        gen = captchaGenerator.generateImage()
        img = gen[0]
        answer = gen[1]

        cacheManager.cacheImage(answer, img)

    requestCounter+=1



    tag = binascii.hexlify(os.urandom(16)).decode("utf-8")
    cache[tag] = answer


    resp = json.dumps({"responseCode": 0, "tag": tag, "img": img})

    return resp

@app.route("/captcha/solve", methods=['POST'])
def solve():
    if "tag" not in request.json:
        resp = json.dumps({"responseCode": 1, "errorMessage": "Missing tag!"})
        return resp

    if "answer" not in request.json:
        resp = json.dumps({"responseCode": 2, "errorMessage": "Missing answer!"})

    tag = request.json["tag"]
    attempt = request.json["answer"]

    if tag not in cache:
        resp = json.dumps({"responseCode": -1, "errorMessage": "TAG doesn't exist or captcha expired, please try again."})
        return resp

    if int(attempt) == cache[tag]:
        resp = json.dumps({"responseCode": 0, "message": "Solved successfully!"})
        return resp

    del cache[tag]
    resp = json.dumps({"responseCode": -2, "errorMessage": "Inccorect answer, please try again."})
    return resp




if __name__ == "__main__":
    app.run(host=host, port=port, debug=False,use_reloader=False)
