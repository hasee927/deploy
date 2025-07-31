import datetime, requests, re, httpx
from core.crud import DalBase
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas
from sqlalchemy import select
from fastapi.encoders import jsonable_encoder



class BotDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(BotDal, self).__init__()
        self.db = db
        self.model = models.BotGroup
        self.schema = schemas.BotGroupSchemasOut

    # 群发消息
    async def senderMsg(self, data):
        if data['msgType'] == '1':
            #商户
            sql = select(self.model).where(self.model.bot_sign == 'merchantBot')
        else:
            #渠道
            sql = select(self.model).where(self.model.bot_sign == 'channelBot')

        queryset = await self.db.scalar(sql)

        token = queryset.token
        chatId = queryset.chat_id
        messages = f"{data['textarea']}\n"
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        jsondata = {
            "chat_id": chatId,
            "text": messages
        }
        headers = {"Content-Type": "application/json"}
        await self.read_external_data(url, headers, jsondata)

    async def read_external_data(self, url, headers, jsondata):
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=jsondata)
            return response.text