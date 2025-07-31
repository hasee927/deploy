import aioredis

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from core.crud import DalBase
from sqlalchemy.ext.asyncio import AsyncSession
from aioredis.client import Redis
from utils.checkSign import verificationSign
from . import models, schemas
from application.settings import SYSTEM_KEY as api_key


class ChannelDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(ChannelDal, self).__init__()
        self.db = db
        self.model = models.ChannelDataList
        self.schema = schemas.ChannelSchemasOut

    # 获取大额代收通道选择项
    async def get_large_in_select_datas(self):
        sql = select(self.model).where(self.model.channel_status == 1,self.model.channel_type == 1)
        queryset = await self.db.scalars(sql)
        return [schemas.ChannelOptionsOut.model_validate(i).model_dump() for i in queryset.all()]


    # 获取大额代付通道选择项
    async def get_big_pay_select_datas(self):
        sql = select(self.model).where(self.model.channel_status == 1,self.model.channel_type == 2)
        queryset = await self.db.scalars(sql)
        return [schemas.ChannelOptionsOut.model_validate(i).model_dump() for i in queryset.all()]


    # 获取在线的通道列表
    async def get_Online_ChannelCode(self, sign):
        signStr = ""
        verificationSign(signStr, api_key, sign, '')

        codeList = []
        sql = select(self.model).where(self.model.channel_status == 1)
        queryset = await self.db.execute(sql)
        datas = queryset.scalars().unique().all()
        for item in datas:
            codeList.append(item.channel_code)
        return codeList



    # 上报通道是否在线
    async def get_Status_ChannelCode(self, code, status, rd: Redis):
        if status == 'off':
            await rd.delete(f"APP_{code}")
        else:
            channel_code = f"APP_{code}"
            await rd.set(channel_code, 1)
