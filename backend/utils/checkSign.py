from core.exception import CustomException
from utils.md5 import generate_md5


# 校验签名
def verificationSign(signStr, api_key, sign, creator):
    signStr = f"{signStr}&secret={api_key}"
    print("签名字符串------->", signStr)
    signRes = generate_md5(signStr)
    print("签名-------->", signRes)
    # 本地后台创建订单
    if creator == "localhost":
        print("系统创建订单")
    else:
        # 商户创建订单，判断入参签名是否正确
        if not sign:
            raise CustomException("缺少签名字段！", code=400)
        if sign != signRes:
            raise CustomException("签名不正确！", code=400)

# 生成签名
def md5Sign(signStr, api_key):
    signStr = f"{signStr}&secret={api_key}"
    print("生成签名=======>>>>>", signStr)
    signRes = generate_md5(signStr)
    return signRes