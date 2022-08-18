import time
import tools
import config
import random
import setting
from error import *
from request import http
from loghelper import log
from account import get_account_list


class Genshin:
    def __init__(self) -> None:
        self.headers = {}
        self.headers.update(setting.headers)
        self.headers['DS'] = tools.get_ds(web=True)
        self.headers['Referer'] = 'https://webstatic.mihoyo.com/bbs/event/signin-ys/index.html?bbs_auth_required=true' \
                                  f'&act_id={setting.genshin_Act_id}&utm_source=bbs&utm_medium=mys&utm_campaign=icon'
        self.headers['Cookie'] = config.config["account"]["cookie"]
        self.headers['x-rpc-device_id'] = tools.get_device_id()
        self.account_list = get_account_list("hk4e_cn", self.headers)
        if len(self.account_list) != 0:
            self.checkin_rewards = self.get_checkin_rewards()

    # 获取已经签到奖励列表
    def get_checkin_rewards(self) -> list:
        log.info("正在获取签到奖励列表...")
        req = http.get(setting.genshin_checkin_rewards, headers=self.headers)
        data = req.json()
        if data["retcode"] != 0:
            log.warning("获取签到奖励列表失败")
            print(req.text)
        return data["data"]["awards"]

    # 判断签到
    def is_sign(self, region: str, uid: str) -> dict:
        req = http.get(setting.genshin_Is_signurl.format(setting.genshin_Act_id, region, uid), headers=self.headers)
        data = req.json()
        if data["retcode"] != 0:
            log.warning("获取账号签到信息失败！")
            print(req.text)
            config.config["games"]["cn"]["genshin"]["auto_checkin"] = False
            config.save_config()
            raise CookieError("BBS Cookie Errror")
        return data["data"]

    def check_in(self, account):
        for i in range(3):
            req = http.post(url=setting.genshin_Signurl, headers=self.headers,
                            json={'act_id': setting.genshin_Act_id, 'region': account[2], 'uid': account[1]})
            data = req.json()
            if data["retcode"] == 0 and data["data"]["success"] == 1:
                time.sleep(random.randint(4, 10))
            else:
                break
        return req

    # 签到
    def sign_account(self) -> str:
        return_data = "原神: "
        if len(self.account_list) != 0:
            for i in self.account_list:
                if i[1] in config.config["games"]["cn"]["genshin"]["black_list"]:
                    continue
                log.info(f"正在为旅行者{i[0]}进行签到...")
                time.sleep(random.randint(2, 8))
                is_data = self.is_sign(region=i[2], uid=i[1])
                if is_data["first_bind"]:
                    log.warning(f"旅行者{i[0]}是第一次绑定米游社，请先手动签到一次")
                else:
                    sign_days = is_data["total_sign_day"] - 1
                    ok = True
                    if not is_data["is_sign"]:
                        log.info(f"旅行者{i[0]}今天已经签到过了~\r\n今天获得的奖励是{tools.get_item(self.checkin_rewards[sign_days])}")
                        sign_days += 1
                    else:
                        time.sleep(random.randint(2, 8))
                        req = self.check_in(i)
                        data = req.json()
                        if data["retcode"] == 0 and data["data"]["success"] == 0:
                            log.info(f"旅行者{i[0]}签到成功~\r\n今天获得的奖励是"
                                     f"{tools.get_item(self.checkin_rewards[0 if sign_days == 0 else sign_days + 1])}")
                            sign_days += 2
                        elif data["retcode"] == -5003:
                            log.info(f"旅行者{i[0]}今天已经签到过了~\r\n今天获得的奖励是{tools.get_item(self.checkin_rewards[sign_days])}")
                        else:
                            s = "账号签到失败！"
                            if data["data"] != "" and data.get("data").get("success", -1):
                                s += "原因: 验证码\njson信息:" + req.text
                            log.warning(s)
                            ok = False
                    if ok:
                        return_data += f"\n{i[0]}已连续签到{sign_days}天\n" \
                                       f"今天获得的奖励是{tools.get_item(self.checkin_rewards[sign_days - 1])}"
                    else:
                        return_data += f"\n{i[0]}，本次签到失败"
                        if data["data"] != "" and data["data"]["success"] == 1:
                            return_data += "，失败原因: 触发验证码"
        else:
            log.warning("账号没有绑定任何原神账号！")
            return_data += "\n并没有绑定任何原神账号"
        return return_data
