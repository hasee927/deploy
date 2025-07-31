from fastapi.encoders import jsonable_encoder
from application.settings import SYSTEM_KEY as api_key
from core.crud import DalBase
from sqlalchemy.ext.asyncio import AsyncSession
from utils.checkSign import verificationSign
from . import models, schemas
from sqlalchemy import select, text, func
from datetime import datetime, timedelta
from ..collectionorder.models import Collect_Order
from ..proxypayorder.models import Proxy_Pay_Order


class SuccessOrderDal(DalBase):
    def __init__(self, db: AsyncSession):
        super(SuccessOrderDal, self).__init__()
        self.db = db
        self.model = models.Order_Success
        self.schema = schemas.SuccessOrderSchemasOut


    # 机器人获取成功订单
    async def getBotSuccessOrder(self, min, signParams):
        # 校验签名
        sign = ""
        try:
            sign = signParams
        except:
            pass

        signStr = f"min={min}"
        verificationSign(signStr, api_key, sign, '')


        ten_minutes_ago = datetime.now() - timedelta(minutes=min)
        sql = select(self.model).where(self.model.create_datetime >= ten_minutes_ago)
        queryset = await self.db.execute(sql)
        datas = queryset.scalars().unique().all()
        return jsonable_encoder(datas)


    # 今日代收统计
    async def get_today_collection(self):
        yestDict = {}
        success_rate = 0
        count = 0
        total = 0
        total_amount = 0
        # 统计今天的数据
        sql = text("select sum(amount) as amount,sum(case status when 1 then 1 end) as success, COUNT(merchant_id) as total \
                   from yg_collection_order WHERE DATE(create_datetime) = CURRENT_DATE;")
        queryset = await self.db.execute(sql)
        result = queryset.fetchall()
        for row in result:
            list_data = [x for x in row]
            if list_data[1]:
                successrate = int(list_data[1]) / int(list_data[2])
                value = round(successrate, 6)
                success_rate = f"{value:.2%}"
                count = list_data[1]
                total = list_data[2]
                total_amount = round(list_data[0],2)

            todayDict = { "success_rate": success_rate, "total_amount": total_amount, "count": count, "total": total }


            # 统计昨天的数据
            sql_yestday = text("select sum(amount) as amount,sum(case status when 1 then 1 end) as success, COUNT(merchant_id) as total \
                               from yg_collection_order WHERE DATE(create_datetime) = CURRENT_DATE - INTERVAL 1 DAY;")
            queryset = await self.db.execute(sql_yestday)
            result = queryset.fetchall()

            for row in result:
                list_data = [x for x in row]
                if list_data[1]:
                    successrate = int(list_data[1]) / int(list_data[2])
                    value = round(successrate, 6)
                    success_rate = f"{value:.2%}"
                    count = list_data[1]
                    total = list_data[2]
                    total_amount = round(list_data[0], 2)

                yestDict = { "success_rate": success_rate, "total_amount": total_amount, "count": count, "total": total }

            tempDict = {"today": todayDict, "yesterday": yestDict}

            return jsonable_encoder(tempDict)


    # 代收排行榜
    async def get_collection_ranking(self):
        sql = text(f"select merchant_id,sum(case status when 1 then 1 else 0 end) as success, COUNT(merchant_id) as total \
                    from yg_collection_order WHERE DATE(create_datetime) = CURRENT_DATE GROUP BY merchant_id;")
        queryset = await self.db.execute(sql)
        result = queryset.fetchall()
        count = len(result)
        tempList = []
        for row in result:
            list_data = [x for x in row]
            successrate = int(list_data[1]) / int(list_data[2])
            value = round(successrate, 6)
            success_rate = f"{value:.2%}"

            sql = select(func.count(Collect_Order.merchant_id)).where(Collect_Order.merchant_id == list_data[0]).where(func.date(Collect_Order.create_datetime) == func.date(func.now()))
            obj = await self.db.scalar(sql)

            tempList.append({"merchant_id": list_data[0], "today_count": list_data[2], "today_success_rate": success_rate, "total": obj})

        return (jsonable_encoder(tempList), count)


    # 今日代付统计
    async def get_today_payout(self):
        yestDict = {}
        success_rate = 0
        count = 0
        total = 0
        total_amount = 0
        # 统计今天的数据
        sql = text("select sum(amount) as amount,sum(case status when 1 then 1 end) as success, COUNT(merchant_id) as total \
                          from yg_proxypay_order WHERE DATE(create_datetime) = CURRENT_DATE;")
        queryset = await self.db.execute(sql)
        result = queryset.fetchall()

        for row in result:
            list_data = [x for x in row]

            if list_data[0]:
                if list_data[1]:
                    successrate = int(list_data[1]) / int(list_data[2])
                    value = round(successrate, 6)
                    success_rate = f"{value:.2%}"
                    count = list_data[1]
                else:
                    success_rate = f"0"
                    count = 0
                total = list_data[2]
                total_amount = round(list_data[0], 2)

            todayDict = {"success_rate": success_rate, "total_amount": total_amount, "count": count, "total": total}

            # 统计昨天的数据
            ytotal_amount = 0
            ycount = 0
            ytotal = 0
            ysuccess_rate = 0
            sql_yestday = text("select sum(amount) as amount,sum(case status when 1 then 1 end) as success, COUNT(merchant_id) as total \
                                      from yg_proxypay_order WHERE DATE(create_datetime) = CURRENT_DATE - INTERVAL 1 DAY;")
            queryset = await self.db.execute(sql_yestday)
            result = queryset.fetchall()
            for row in result:
                list_data = [x for x in row]
                if list_data[0]:
                    if list_data[1]:
                        successrate = int(list_data[1]) / int(list_data[2])
                        value = round(successrate, 6)
                        ysuccess_rate = f"{value:.2%}"
                        ycount = list_data[1]
                    ytotal = list_data[2]
                    ytotal_amount = round(list_data[0], 2)

                yestDict = {"success_rate": ysuccess_rate, "total_amount": ytotal_amount, "count": ycount, "total": ytotal}

            tempDict = {"today": todayDict, "yesterday": yestDict}

            return jsonable_encoder(tempDict)


    # 代付排行榜
    async def get_payout_ranking(self):
        sql = text(f"select merchant_id,sum(case status when 1 then 1 else 0 end) as success, COUNT(merchant_id) as total \
                            from yg_proxypay_order WHERE DATE(create_datetime) = CURRENT_DATE GROUP BY merchant_id;")
        queryset = await self.db.execute(sql)
        result = queryset.fetchall()
        count = len(result)
        tempList = []
        for row in result:
            list_data = [x for x in row]
            successrate = int(list_data[1]) / int(list_data[2])
            value = round(successrate, 6)
            success_rate = f"{value:.2%}"

            sql = select(func.count(Proxy_Pay_Order.merchant_id)).where(Proxy_Pay_Order.merchant_id == list_data[0]).where(func.date(Proxy_Pay_Order.create_datetime) == func.date(func.now()))
            obj = await self.db.scalar(sql)

            tempList.append({"merchant_id": list_data[0], "today_count": list_data[2], "today_success_rate": success_rate, "total": obj})

        return (jsonable_encoder(tempList), count)



    # 统计代付pendding金额
    async def get_paypending_data(self):
        sql = select(func.sum(Proxy_Pay_Order.amount)).where(Proxy_Pay_Order.status == 0)
        obj = await self.db.scalar(sql)
        if not obj:
            obj = 0
        return obj
