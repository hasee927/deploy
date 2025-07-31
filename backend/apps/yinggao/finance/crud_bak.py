from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from core.exception import CustomException
from core.crud import DalBase
from . import models, schemas
from sqlalchemy import select, func, update
from sqlalchemy.dialects.mysql import insert
from ..merchantlist.models.mtlist import MerchantList
from ..collectionorder.models.collorder import Collect_Order
from ..proxypayorder.models.pporder import Proxy_Pay_Order
from decimal import Decimal

class FinanceDal(DalBase):
    def __init__(self, db: AsyncSession):
        super(FinanceDal, self).__init__()
        self.db = db
        self.model = models.Finance
        self.schema = schemas.FinanaceSchemasOut



    # 获取商户资金列表
    async def getFinanceData(self, page: int = 1,limit: int = 10,v_order: str = None,v_order_field: str = None,**kwargs):
        # 查询代收成功金额
        # select merchant_id,sum(entry_amount) as entry_amount from yg_collection_order WHERE status = 1 GROUP BY merchant_id;
        sql_coll = select(Collect_Order.merchant_id,func.sum(Collect_Order.entry_amount)).where(Collect_Order.status == 1).group_by(Collect_Order.merchant_id)
        queryset = await self.db.execute(sql_coll)
        change_fund_datas = queryset.unique().all()

        # 统计在途金额（pending）
        # select merchant_id,sum(amount) as amount from yg_proxypay_order WHERE status = 0 GROUP BY merchant_id;
        sql_coll = select(Proxy_Pay_Order.merchant_id, func.sum(Proxy_Pay_Order.amount)).where(Proxy_Pay_Order.status == 0).group_by(Proxy_Pay_Order.merchant_id)
        queryset = await self.db.execute(sql_coll)
        pay_datas = queryset.unique().all()


        # 查找商户列表，并初始化
        sql = select(MerchantList)
        queryset = await self.db.execute(sql)
        datas = queryset.scalars().unique().all()
        merchantList = []
        for row in datas:
            merchantList.append({ "merchant_id": row.merchant_id, "total_amount": 0, "change_fund": 0, "pending_amount": 0 })


        print("merchantList----->>>>", merchantList)

        # 统计成功的代收金额 和 在途金额(pending)
        for row in merchantList:
            merchant_id = row['merchant_id']
            for item in change_fund_datas:
                tempList = list(item)
                if merchant_id == tempList[0]:
                    row['change_fund'] = float(Decimal(float(tempList[1])).quantize(Decimal("0.0000")))

            for item in pay_datas:
                tempList2 = list(item)
                if merchant_id == tempList2[0]:
                    row['pending_amount'] = float(Decimal(float(tempList2[1])).quantize(Decimal("0.0000")))

            # 计算总金额
            sql_finan = select(self.model).where(self.model.merchant_id == merchant_id)
            obj = await self.db.scalar(sql_finan)
            if obj:
                row['change_fund'] = float(row['change_fund']) - float(obj.deduct) + float(obj.add)
                row['total_amount'] = float(row['change_fund'] + row['pending_amount'])
            else:
                row['total_amount'] = float(row['change_fund'] + row['pending_amount'])


        print("merchantList----->>>>", merchantList)


        # 插入商户资金数据
        for row in merchantList:
            perData = {"merchant_id": row['merchant_id'], "total_amount": row['total_amount'], "change_fund": row['change_fund'], 'pending_amount': row['pending_amount'] }
            insert_stmt = insert(self.model).values(**perData)
            on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(**perData)
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
            # 划扣
            # if data.change_type == 0:
            #     if float(obj.change_fund) != 0:
            #         change_fund = float(obj.change_fund) - float(data.change_amount)
            #         total_amount = float(obj.total_amount) - float(data.change_amount)
            #         obj.change_fund = float(Decimal(float(change_fund)).quantize(Decimal("0.0000")))
            #         obj.total_amount = float(Decimal(float(total_amount)).quantize(Decimal("0.0000")))
            #         obj.change_type = data.change_type
            #         obj.change_amount = data.change_amount
            #         await self.db.flush()
            #     else:
            #         raise CustomException("没有可转换资金！", code=400)
            #
            # if data.change_type == 1:
            #     print("调账----------->>>>", data)
            #
            # if data.change_type == 2:
            #     print("调账----------->>>>", data)
            #
            # if data.change_type == 3:
            #     print("调账----------->>>>", data)
            pass

            if float(obj.change_fund) != 0:
                obj.change_type = data.change_type
                obj.change_amount = data.change_amount
                if data.change_type == 0:
                    # 划扣
                    obj.deduct = data.change_amount

                if data.change_type == 1:
                    # 上分
                    obj.add = data.change_amount

                if data.change_type == 2:
                    # 可用转代付
                    obj.used_pay = data.change_amount

                if data.change_type == 3:
                    # 代付转可用
                    obj.pay_used = data.change_amount

                await self.db.flush()

        return "调账成功"