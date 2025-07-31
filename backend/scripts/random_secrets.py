# 生成随机数

import random
import string


def generate_random_string(length):
    # 定义所有可能的字符
    characters = string.ascii_letters + string.digits  # 包含所有大小写字母和数字
    # 可以选择添加特殊字符，例如：string.punctuation
    # characters += string.punctuation

    # 使用random.choices生成随机字符串
    random_string = ''.join(random.choices(characters, k=length))
    return random_string


# 生成一个长度为10的随机字符串
random_string = generate_random_string(24)
print(random_string)