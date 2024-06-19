import os
import time
import signal
import datetime
import math
import random
from loghelper import log

from crontab import CronTab

time_format = "%Y-%m-%d %H:%M:%S"

# 获取当前文件的绝对路径
current_file = os.path.abspath(__file__)

# 获取当前文件所在的目录
current_directory = os.path.dirname(current_file)

# 修改运行目录为当前文件所在的目录
os.chdir(current_directory)
log.info("运行目录:" + current_directory)


def stop_me(_signo, _stack):
    log.info("Docker container has stoped....")
    exit(-1)


def next_run_time():
    # 获取当前日期和时间
    current_datetime = datetime.datetime.now()
    # 获取当前日期
    current_date = current_datetime.date()
    # 计算下一天的日期
    next_date = current_date + datetime.timedelta(days=1)
    # 设置上午9点作为起始时间
    start_time = datetime.datetime.combine(next_date, datetime.time(8, 0))
    # 设置晚上10点作为结束时间
    end_time = datetime.datetime.combine(next_date, datetime.time(10, 0))
    # 生成随机时间
    random_time = start_time + \
                  datetime.timedelta(minutes=random.randint(
                      0, (end_time - start_time).seconds // 60))
    # 计算时间差
    time_diff = random_time - current_datetime
    # 获取剩余秒数
    remaining_seconds = math.ceil(time_diff.total_seconds())
    log.info("下一天的时间范围：")
    log.info(f"起始时间：{start_time}")
    log.info(f"结束时间：{end_time}")
    log.info(f"随机时间：{random_time}")
    log.info(f"剩余秒数：{remaining_seconds}")
    return remaining_seconds


def main():
    signal.signal(signal.SIGINT, stop_me)
    log.info("使用DOCKER运行米游社签到")
    env = os.environ

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
