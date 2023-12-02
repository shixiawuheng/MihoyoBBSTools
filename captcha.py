from geetest.ttocr import TTOCR

gt3 = TTOCR("e52c9331b81f7d7ddca00afd2cbcaba1")


def game_captcha(gt: str, challenge: str):
    params = {
        gt: gt,
        challenge: challenge
    }
    res = gt3.run(gt, challenge)
    if res:
        return res.get("validate"), res.get("challenge")
    return None, None  # 失败返回None 成功返回validate


def bbs_captcha(gt: str, challenge: str):
    params = {
        gt: gt,
        challenge: challenge
    }
    res = gt3.run(gt, challenge)
    if res:
        return res.get("validate"), res.get("challenge")
    return None, None  # 失败返回None 成功返回validate
