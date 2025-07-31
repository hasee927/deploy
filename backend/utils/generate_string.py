import random
import string


def generate_random_string(length=6):
    """
    生成一个指定长度的随机字符串，包含大小写字母和数字。
    :param length: 字符串的长度，默认为10。
    :return: 一个随机字符串。
    """
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


# # 使用示例
# random_string = generate_random_string()
# print(random_string)


# 随机生成10个大小写字符串
def generate_email_string(length=10):
    letters = string.ascii_letters  # 包含所有大小写字母
    return ''.join(random.choice(letters) for i in range(length))


# random_string = generate_email_string(10)
# print(random_string)
