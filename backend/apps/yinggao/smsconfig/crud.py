import datetime, requests, re, httpx
from core.crud import DalBase
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas
from sqlalchemy import select
from fastapi.encoders import jsonable_encoder
from .utils.tools import getOtpCode
from ..botconfig.models import BotConfig


class SmsDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(SmsDal, self).__init__()
        self.db = db
        self.model = models.SmsList
        self.schema = schemas.SmsSchemasOut

class SmsPostDal(DalBase):
    def __init__(self, db: AsyncSession):
        super(SmsPostDal, self).__init__()
        self.db = db
        self.model = models.SmsList
        self.schema = schemas.SmsSchemasOut

    # 添加短信内容---对外提供接口---不需要token验证
    async def addSmsData(self, data):
        # print("短信数据------>", data)

        if len(data['data']) == 0:
            return

        # 查找发送短信的机器人
        sql = select(BotConfig).where(BotConfig.bot_sign == 'sms')
        queryset = await self.db.scalar(sql)


        for item in data['data']:
            # sms_type: 1，其他短信 2，OTP短信
            sms_type = 1
            otpCode = ''
            smsContext = item['body']

            timestamp = float(item['date']) / 1000.0  # 输入要转换的时间戳
            dt_object = datetime.datetime.fromtimestamp(timestamp)
            formatted_date = dt_object.strftime('%Y-%m-%d %H:%M:%S')  # 格式化日期时间

            # "LLFL" 是 gte 登录验证码
            if smsContext.find("OTP") > -1 or smsContext.find("LLFL") > -1:
                sms_type = 2
                otpCode = getOtpCode(item['channel_code'], smsContext)
                try:
                    # 发送otp到机器人
                    token = queryset.token
                    chatId = queryset.chat_id
                    messages = f"\n【OTP短信消息】\n通道代码: {item['channel_code']}\nOTP: {otpCode}\n短信时间: {formatted_date}\n短信内容: {item['body']}\n"
                    url = f"https://api.telegram.org/bot{token}/sendMessage"
                    jsondata = {
                        "chat_id": chatId,
                        "text": messages
                    }
                    headers = {"Content-Type": "application/json"}
                    await self.read_external_data(url, headers, jsondata)
                except:
                    pass

            # 写入银行流水数据库， 待做


            # 写入数据库
            tmpData = {
                "sms_id": item['_id'],
                "channel_code": item['channel_code'],
                "sender_addr": item['address'],
                "sms_time": formatted_date,
                "sms_utc_time": item['date'],
                "sms_type": sms_type,
                "code": otpCode,
                "context": item['body'],
            }
            obj = self.model(**tmpData)
            self.db.add(obj)

        await self.db.commit()
        return "添加成功"



    async def read_external_data(self, url, headers, jsondata):
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=jsondata)
            print(response.text)




    # 根据短信ID查询是否存在
    async def getSmsIdData(self, sms_id):
        sql = select(self.model).where(self.model.sms_id == str(sms_id))
        queryset = await self.db.scalar(sql)
        return jsonable_encoder(queryset)
