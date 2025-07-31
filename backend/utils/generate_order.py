import time
import random


def generate_order_number(starNo):
    # 时间戳
    # timestamp = str(int(time.time()))
    # 随机数
    random_num = str(random.randint(10000000000000, 99999999999999))
    # 组合订单号
    order_number = f"{starNo}{random_num}"
    return order_number
