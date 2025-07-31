from core.crud import DalBase
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select


class BankWaterDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(BankWaterDal, self).__init__()
        self.db = db
        self.model = models.BankWater
        self.schema = schemas.BankWaterSchemasOut

    # async def get_select_datas(self) -> list:
    #     """
    #     获取选择数据，全部数据
    #     :return:
    #     """
    #     sql = select(self.model)
    #     queryset = await self.db.scalars(sql)
    #
    #     return [schemas.BankWaterOptions.model_validate(i).model_dump() for i in queryset.all()]