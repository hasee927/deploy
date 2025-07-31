import httpx, asyncio
from core.crud import DalBase
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas
from sqlalchemy import select
from fastapi.encoders import jsonable_encoder

from ..botgroup.models import BotGroup



class BotDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(BotDal, self).__init__()
        self.db = db
        self.model = models.BotConfig
        self.schema = schemas.BotSchemasOut

    # 群发消息
    async def senderMsg(self, data):
        if data['msgType'] == '1':
            #商户
            sql = select(self.model).where(self.model.bot_sign == 'merchantBot')
            sql_group = select(BotGroup.chat_id).where(BotGroup.disabled).where(BotGroup.type == 1)

        else:
            #渠道
            sql = select(self.model).where(self.model.bot_sign == 'channelBot')
            sql_group = select(BotGroup.chat_id).where(BotGroup.disabled).where(BotGroup.type == 2)

        queryset = await self.db.scalar(sql)
        token = queryset.token
        messages = f"{data['textarea']}\n"
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        ids = await self.db.scalars(sql_group)
        await asyncio.gather(*(self.read_external_data(url, chatId, messages) for chatId in ids))


    async def read_external_data(self, url, chatId, messages):
        headers = {"Content-Type": "application/json"}
        async with httpx.AsyncClient() as client:
            jsondata = {
                "chat_id": chatId,
                "text": messages
            }

            response = await client.post(url, headers=headers, json=jsondata)
            return response.text