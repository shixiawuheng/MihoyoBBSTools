import datetime
import math
import random

# 获取当前日期和时间
current_datetime = datetime.datetime.now()

# 获取当前日期
current_date = current_datetime.date()

# 计算下一天的日期
next_date = current_date + datetime.timedelta(days=1)

# 设置上午9点作为起始时间
start_time = datetime.datetime.combine(next_date, datetime.time(9, 0))

# 设置晚上10点作为结束时间
end_time = datetime.datetime.combine(next_date, datetime.time(22, 0))

# 生成随机时间
random_time = start_time + datetime.timedelta(minutes=random.randint(0, (end_time - start_time).seconds // 60))

# 计算时间差
time_diff = random_time - current_datetime

# 获取剩余秒数
remaining_seconds = math.ceil(time_diff.total_seconds())

print("下一天的时间范围：")
print("起始时间：", start_time)
print("结束时间：", end_time)
print("随机时间：", random_time)
print("剩余秒数：", remaining_seconds)
