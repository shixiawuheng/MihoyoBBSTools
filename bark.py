import requests


def GetLevel(res):
    # active 亮屏
    # timeSensitive 时效
    # passive 静默
    if len(res['error']):
        return 'active'
    return 'passive'


def bark(resp, msg):
    data = {
        'group': "miyoushe",
        'title': "米游社签到",
        'body': msg,
        'level': GetLevel(resp)
    }
    res = requests.post("https://api.day.app/nsKRTSwc2jd39ozxkrnTK6", data).json()
    if res.get("code") == 200:
        pass
    # res = requests.post("https://api.day.app/nsKRTSwc2jd39ozxkrnTK6", data).json()
    # if res.get("code") == 200:
    #     pass


if __name__ == '__main__':
    results = {
        "ok": [],
        "close": [],
        "error": [],
        "captcha": []
    }
    push_message = f'脚本执行完毕，共执行{0}个配置文件，成功{len(results["ok"])}个，' \
                   f'没执行{len(results["close"])}个，失败{len(results["error"])}个' \
                   f'\r\n没执行的配置文件: {results["close"]}\r\n执行失败的配置文件: {results["error"]}\r\n' \
                   f'触发游戏签到验证码的配置文件: {results["captcha"]} '
    bark(results, push_message)
