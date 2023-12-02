import os
import time
import signal
import datetime
from loghelper import log
import random

time_format = "%Y-%m-%d %H:%M:%S"


def stop_me(_signo, _stack):
    log.info("Docker container has stoped....")
    exit(-1)


def main():
    signal.signal(signal.SIGINT, stop_me)
    log.info("使用DOCKER运行米游社签到")
    env = os.environ
    cron_signin = env["CRON_SIGNIN"]
    # cron = CronTab(cron_signin, loop=True, random_seconds=True)

    # def next_run_time_bak():
    #     # 生成随机的小时部分取值范围
    #     random_hour = random.randint(9, 21)
    #     random_m = random.randint(0,59)
    #     # 设置 cron 表达式为每天上午9点到晚上10点之间的随机时间点
    #     cron_signin = f"{random_m} {random_hour} * * *"
    #     cron.set(cron_signin)
    #     nt = datetime.datetime.now().strftime(time_format)
    #     delayt = cron.next(default_utc=False)
    #     nextrun = datetime.datetime.now() + datetime.timedelta(seconds=delayt)
    #     nextruntime = nextrun.strftime(time_format)
    #     log.info(f"Current running datetime: {nt}")
    #     log.info(f"Next run datetime: {nextruntime}")

    def next_run_time():
        # 生成随机的小时部分取值范围
        random_hour = random.randint(9, 21)
        random_m = random.randint(0,59)
        # 设置 cron 表达式为每天上午9点到晚上10点之间的随机时间点
        cron_signin = f"{random_m} {random_hour} * * *"
        cron.set(cron_signin)
        nt = datetime.datetime.now().strftime(time_format)
        delayt = cron.next(default_utc=False)
        nextrun = datetime.datetime.now() + datetime.timedelta(seconds=delayt)
        nextruntime = nextrun.strftime(time_format)
        log.info(f"Current running datetime: {nt}")
        log.info(f"Next run datetime: {nextruntime}")


    def sign():
        log.info("Starting signing")
        multi = env["MULTI"].upper()
        if multi == 'TRUE':
            os.system("python3 ./main_multi.py autorun")
        else:
            os.system("python3 ./main.py")

    
    
    while True:
        sign()
        time.sleep(next_run_time())
        


if __name__ == '__main__':
    main()
