import requests


# gt3 = TTOCR("e52c9331b81f7d7ddca00afd2cbcaba1")


def game_captcha(gt: str, challenge: str):
    params = {
        "gt": gt,
        "challenge": challenge
    }
    try:
        res = requests.post("http://47.104.229.158:18754/jy3", params).json()
        if res and res.get("code") == 1:
            res = res.get("data")
            return res.get("validate"), res.get("challenge")
    except Exception as e:
        pass
    return None, None  # 失败返回None 成功返回validate


def bbs_captcha(gt: str, challenge: str):
    params = {
        "gt": gt,
        "challenge": challenge
    }
    # res = gt3.run(gt, challenge)
    try:
        res = requests.post("http://47.104.229.158:18754/jy3", params).json()
        if res and res.get("code") == 1:
            res = res.get("data")
            return res.get("validate"), res.get("challenge")
    except Exception as e:
        pass
    return None, None  # 失败返回None 成功返回validate


if __name__ == "__main__":
    params = {
        "gt": "132456",
        "challenge": "123456"
    }
    res = requests.post("http://192.168.1.11:18754/jy3", params).json()
