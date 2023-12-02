#!/usr/bin/env python
# coding:utf-8
import time

import requests


class TTOCR(object):
    def __init__(self, appkey):
        self.base_params = {
            'appkey': appkey,
            'itemid': "388",
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def post(self, gt: str, challenge: str):
        params = {
            'gt': gt,
            'challenge': challenge
        }
        params.update(self.base_params)
        res = requests.post("http://api.ttocr.com/api/recognize", params).json()
        if res.get("status") == 1:
            return res.get("resultid")
        print(res.get("msg"))
        return ""

    def results(self, id: str):
        params = {
            'resultid': id,
        }
        params.update(self.base_params)
        res = requests.post("http://api.ttocr.com/api/results", params).json()
        if res.get("status") == 1:
            return res.get("data")
        print(res.get("msg"))
        return None

    def run(self, gt: str, challenge: str):
        res = self.post(gt, challenge)
        if res != "":
            val = None
            count = 1
            while val is None:
                count = count + 1
                if count > 30:
                    break
                val = self.results(res)
                time.sleep(2)
                if val is -1:
                    return None
            if val:
                return val
        return None


if __name__ == '__main__':
    ocr = TTOCR("e52c9331b81f7d7ddca00afd2cbcaba1")
    ocr.run("245273d7fa73f7b657098bf7441fe12f", "30f0f04fe984bce964de5749c9f17099")
