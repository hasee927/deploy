import time
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from core.exception import CustomException
from core.crud import DalBase
from utils.generate_order import generate_order_number
from . import models, schemas
from sqlalchemy import select, func, update
from sqlalchemy.dialects.mysql import insert

from ..fundwater.help import HelpFundWaterDal
from ..merchantlist.models.mtlist import MerchantList
from ..fundwater.models.fundwater import FundWater
from decimal import Decimal

class FinanceDal(DalBase):
    def __init__(self, db: AsyncSession):
        super(FinanceDal, self).__init__()
        self.db = db
        self.model = models.Finance
        self.schema = schemas.FinanaceSchemasOut



    # 获取商户资金列表
    async def getFinanceData(self, page: int = 1,limit: int = 10,v_order: str = None,v_order_field: str = None,**kwargs):
        # 查找商户列表，并初始化
        sql = select(MerchantList)
        queryset = await self.db.execute(sql)
        datas = queryset.scalars().unique().all()
        merchantList = []
        for row in datas:
            merchantList.append({ "merchant_id": row.merchant_id, "total_amount": 0, "change_fund": 0, "pay_amount": 0,"pending_amount": 0 })


        # 插入商户资金数据
        for row in merchantList:
            merchant_id = row['merchant_id']
            # 到流水表中查找商户最大id
            sql = select(FundWater).where(FundWater.merchant_id == merchant_id).order_by(FundWater.id.desc()).limit(1)
            obj = await self.db.scalar(sql)
            if obj:
                perData = {"merchant_id": row['merchant_id'], "total_amount": obj.change_total_amount,
                           "pay_amount": obj.change_pay_amount,"change_fund": obj.change_fund, 'pending_amount': obj.change_pending_amount }
                insert_stmt = insert(self.model).values(**perData)
                on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(**perData)
            else:
                insert_stmt = insert(self.model).values(**row)
                on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(**row)

            await self.db.execute(on_duplicate_key_stmt)
            await self.db.flush()

        # 获取数据总数
        count_sql = select(func.count(self.model.id))
        count_queryset = await self.db.execute(count_sql)
        count = count_queryset.one()[0]

        # 条件查询
        conditions = []
        for field, value in kwargs.items():
            attr = getattr(self.model, field)
            if value[0] == "like" and value[1]:
                conditions.append(attr.like(f"%{value[1]}%"))

        sql_finance = select(self.model).where(*conditions)
        if limit != 0:
            sql_finance = sql_finance.offset((page - 1) * limit).limit(limit)
        queryset = await self.db.scalars(sql_finance)
        res = queryset.unique().all()
        return (jsonable_encoder(res), count)


    # 调账
    async def update_finance_data(self, data_id, data):
        sql = select(self.model).where(self.model.id == data_id)
        obj = await self.db.scalar(sql)
        if obj:
            nowDate = time.strftime("%Y-%m-%d %X", time.localtime())
            # 流水实例化
            fund = HelpFundWaterDal(self.db)
            order_id = generate_order_number(60066)

            # if float(obj.change_fund) != 0:

            if data.change_type == 0:
                if float(data.change_amount) > float(obj.change_fund):
                    raise CustomException("金额不足!", code=400)
                data.change_amount = -float(data.change_amount)

            if data.change_type == 2:
                if float(data.change_amount) > float(obj.change_fund):
                    raise CustomException("金额不足!", code=400)

            if data.change_type == 3:
                if float(data.change_amount) > float(obj.pay_amount):
                    raise CustomException("金额不足!", code=400)


            # 记流水
            await fund.add_fund_water(obj.merchant_id, data.change_type, order_id, data.change_amount, nowDate)

            # else:
            #     raise CustomException("金额不足!", code=400)

        return "调账成功"