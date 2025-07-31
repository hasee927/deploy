import time, os
from core.crud import DalBase
from sqlalchemy.ext.asyncio import AsyncSession
from core.exception import CustomException
from utils.file.file_base import FileBase
from . import models, schemas
from utils import status
from fastapi import FastAPI
import asyncio
import async_timeout
import aioredis
from fastapi.encoders import jsonable_encoder
from .help.help import upload_data
from sqlalchemy.dialects.mysql import insert



app = FastAPI()  # pylint: disable=invalid-name

from pydantic import BaseModel


class MessageEvent(BaseModel):
    username: str
    message: dict



async def reader(channel: aioredis.client.PubSub):
    for i in range(15):
        time.sleep(1)
        try:
            async with async_timeout.timeout(1):
                # 执行接收订阅消息
                message = await channel.get_message(ignore_subscribe_messages=True)
                if message is not None:
                    message_event = MessageEvent.parse_raw(message['data'])
                    print("订阅接收到消息为：",message_event)
                await asyncio.sleep(0.01)
        except asyncio.TimeoutError:
            pass



class BKListDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(BKListDal, self).__init__()
        self.db = db
        self.model = models.Banklist
        self.schema = schemas.BKListSchemasOut

    # 接收上传文件----暂时没有登录认证
    async def uploadCsvFile(self, file: any):
        # file_path = FileBase.generate_static_file_path(path='uploads', suffix=None)
        # print("file_path--------->>>>", file_path)

        dirs = 'static/uploads'
        # 判断uploads目录是否存在，否则新建uploads目录
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        # 保存上传文件到uploads目录
        file_location = f"{dirs}/{file.filename}"
        with open(file_location, "wb") as file_object:
            file_object.write(file.file.read())
        return {"filename": file.filename}


    #
    # # 接收上传验证码
    # async def uploadCaptcha(self, file):
    #     dirs = 'static/captcha'
    #     # 判断uploads目录是否存在，否则新建uploads目录
    #     if not os.path.exists(dirs):
    #         os.makedirs(dirs)
    #     # 保存上传文件到uploads目录
    #     file_location = f"{dirs}/{file.filename}"
    #     with open(file_location, "wb") as file_object:
    #         file_object.write(file.file.read())
    #     return {"filename": file.filename}

    # 接收前端手动输入的验证码
    # async def manualCaptchaImageData(self, data):
    #     print("接收前端手动输入的验证码--------->", data["captcha"])
    #     # 保存到本地
    #     captcha_file = 'static/captcha/captcha.txt'
    #     with open(captcha_file, 'w+') as f:
    #         f.write(data["captcha"])
    #         f.flush()
    #         f.close()
    #
    #     return {"file_name": "captcha.txt","captcha":data["captcha"]}

    # # 进入银行系统后清空验证码
    # async def removeCaptchaImageData(self):
    #     captcha_file = 'static/captcha/captcha.txt'
    #     with open(captcha_file, 'w+') as f:
    #         f.close()
    #
    #
    # # 监听redis验证码错误消息，使用发布订阅功能
    # async def listenErrorMsgData(self, data, rd: Redis):
    #     # 获取redis key
    #     # channel = data
    #     # res = await rd.get(channel)
    #     # return  res
    #
    #     # 参考文档 https://blog.itpub.net/70041327/viewspace-3037650/ 和 https://www.cnblogs.com/weiweivip666/p/18041474
    #     app.state.redis = rd
    #     # 创建消息发布定义对象，获取发布订阅对象
    #     pubsub = rd.pubsub()
    #     # 把当前的发布对象添加到全局app上下文中
    #     app.state.pubsub = pubsub
    #     # 把发布方法添加到全局app上下文中
    #     app.state.publish = rd.publish
    #     # 开始订阅相关频道
    #     await pubsub.subscribe(data)
    #     # # 开始订阅相关频道
    #     # await pubsub.subscribe('channel:1', 'channel:2')
    #     # # 消息模型的创建
    #     # event = MessageEvent(username='jack', message={'msg': '在startup_event发布的事件消息'})
    #     # # 把消息发布到channel:1频道上
    #     # await redis.publish(channel='channel:1', message=event.json())
    #     while True:
    #         await asyncio.sleep(0.05)
    #         message = await pubsub.get_message(ignore_subscribe_messages=True)
    #         if message:
    #             print(json.loads(message['data']))
    #             return jsonable_encoder(json.loads(message['data']))
    #             # return json.loads(message['data'])



    ###################################################################################
    # 手动导入流水数据
    async def importCsvFile(self, data: any):
        obj = upload_data(self.db)
        result = await obj.import_csv_data(data)
        return jsonable_encoder(result)


# 添加银行列表数据---对外提供接口---不需要token验证。
class BKListPostDal(DalBase):
    def __init__(self, db: AsyncSession):
        super(BKListPostDal, self).__init__()
        self.db = db
        self.model = models.Banklist
        self.schema = schemas.BKListSchemasOut

    # 添加代收订单---对外提供接口---不需要token验证。
    async def addBKListData(self,  data: any):
        for perData in data:
            try:
                # 去掉金额中的逗号
                tmp_amount = str(perData['amount']).strip(" ")
                amount = str(float(''.join(tmp_amount.split(','))))
                tmp_balance = str(perData['account_balance']).strip(" ")
                balance = str(float(''.join(tmp_balance.split(','))))
                perData['amount'] = amount
                perData['account_balance'] = balance
                insert_stmt = insert(self.model).values(**perData)
                # on_duplicate_key_update 插入数据如果有则更新
                on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(**perData)
                await self.db.execute(on_duplicate_key_stmt)
            except:
                raise CustomException("utr已存在！", code=status.HTTP_ERROR)
        await self.db.commit()
        return "添加成功"


