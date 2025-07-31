from itertools import count

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, create_engine, ScalarResult, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


class BankData:

    def __init__(self, db: AsyncSession, data: any = None):
        self.db = db
        self.data = data
        self.model = models.bank.Bank
        self.schema = schemas.bank.BankSchemasOut

    # 添加银行数据
    async def addBank(self):
        obj = self.model(**self.data.model_dump())
        self.db.add(obj)
        await self.db.commit()
        return "添加成功"

    # 获取银行数据列表
    async def getBanks(self):
        sql = select(self.model).filter(self.model.is_delete == 0)
        # res  =  await self.db.execute(sql)
        # return jsonable_encoder(res.scalars().all())
        queryset: ScalarResult = await self.db.scalars(sql)
        return jsonable_encoder(queryset.all())

    # 获取银行分页数据
    async def getDataPage(
            self,
            page: int = 1,
            limit: int = 10,
            v_order: str = None,
            v_order_field: str = None,
            **kwargs
        ):

        sql = select(self.model)

        # 获取数据总数
        count_sql = select(func.count()).select_from(sql.alias())
        count_queryset = await self.db.execute(count_sql)
        count = count_queryset.one()[0]

        # 条件查询
        conditions = []
        for field, value in kwargs.items():
            attr = getattr(self.model, field)
            if value[0] == "like" and value[1]:
                conditions.append(attr.like(f"%{value[1]}%"))
        sql = sql.where(*conditions)

        if limit != 0:
            sql = sql.offset((page - 1) * limit).limit(limit)

        queryset = await self.db.scalars(sql)
        return jsonable_encoder(queryset.unique().all()), count


    # 根据id获取银行数据
    async def getBankById(self, data_id: int):
        sql = select(self.model).where(self.model.id == data_id)
        queryset: ScalarResult = await self.db.scalar(sql)
        return jsonable_encoder(queryset)



    # 根据id编辑银行数据
    async def editBankById(self, data_id: int, data: any):
        sql = select(self.model).where(self.model.id == data_id)
        obj: ScalarResult = await self.db.scalar(sql)
        obj_dict = jsonable_encoder(data)
        for key, value in obj_dict.items():
            setattr(obj, key, value)
        await self.db.commit()
        return "编辑成功"


    # 根据id删除银行数据
    async def delBankById(self, data_id: int):
        sql = select(self.model).where(self.model.id == data_id)
        obj = await self.db.scalar(sql)
        await self.db.delete(obj)
        await self.db.commit()
        return "删除成功"

