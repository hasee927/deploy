from sqlalchemy.ext.asyncio import AsyncSession
from core.crud import DalBase
from .models.fundwater import FundWater
from sqlalchemy import select, update
from sqlalchemy.dialects.mysql import insert
from decimal import Decimal


class HelpFundWaterDal(DalBase):
    def __init__(self, db: AsyncSession):
        super(HelpFundWaterDal, self).__init__()
        self.db = db
        self.model = FundWater

    # 添加流水
    # 流水类型; 0:划扣, 1:上分, 2:可用转代付 ,3:代付转可用, 4:支付成功, 5:订单冲正, 6:代付pending, 7:代付成功, 8:代付失败
    async def add_fund_water(self,merchant_id, water_type, bill_no, change_amount, optime):
        # print("添加流水---->>>>", merchant_id, water_type, bill_no, change_amount, optime)
        # 查找商户，最大id
        sql = select(self.model).where(self.model.merchant_id == merchant_id).order_by(self.model.id.desc()).limit(1)
        obj = await self.db.scalar(sql)

        # 2，没有数据插入
        # 3，有数据需要找出最大一条数据，然后把这个数据中的值和新数据相加，然后插入

        # 1，判断是否存在merchant_id的数据
        if obj:
            # 可用转代付
            if water_type == 2:
                tmp_change_fund = float(obj.change_fund) - float(change_amount)
                change_fund = Decimal(float(tmp_change_fund)).quantize(Decimal("0.0000"))

                tmp_change_pay_amount = float(obj.change_pay_amount) + float(change_amount)
                change_pay_amount = Decimal(float(tmp_change_pay_amount)).quantize(Decimal("0.0000"))

                change_total_amount = obj.change_total_amount

                oldData = {"merchant_id": merchant_id, "water_type": water_type, "bill_no": bill_no, 'optime': optime,
                           'change_amount': change_amount, 'change_total_amount': change_total_amount,'change_pay_amount': change_pay_amount,
                           'change_fund': change_fund}
                obj = self.model(**oldData)
                self.db.add(obj)

            # 代付转可用
            if water_type == 3:
                tmp_change_fund = float(obj.change_fund) + float(change_amount)
                change_fund = Decimal(float(tmp_change_fund)).quantize(Decimal("0.0000"))

                tmp_change_pay_amount = float(obj.change_pay_amount) - float(change_amount)
                change_pay_amount = Decimal(float(tmp_change_pay_amount)).quantize(Decimal("0.0000"))

                change_total_amount = obj.change_total_amount

                oldData = {"merchant_id": merchant_id, "water_type": water_type, "bill_no": bill_no, 'optime': optime,
                           'change_amount': change_amount, 'change_total_amount': change_total_amount,
                           'change_pay_amount': change_pay_amount,
                           'change_fund': change_fund}
                obj = self.model(**oldData)
                self.db.add(obj)


            # 划扣 或 上分 或 流水类型--->支付成功 或 冲正
            if water_type == 0 or water_type == 1 or water_type == 4 or water_type == 5:
                tmp_change_fund = float(obj.change_fund) + float(change_amount)
                change_fund = Decimal(float(tmp_change_fund)).quantize(Decimal("0.0000"))

                change_pay_amount = obj.change_pay_amount

                tmp_change_total_amount = float(obj.change_pending_amount) + float(obj.change_pay_amount) + float(obj.change_fund) + float(change_amount)
                change_total_amount = Decimal(float(tmp_change_total_amount)).quantize(Decimal("0.0000"))



                oldData = {"merchant_id": merchant_id, "water_type": water_type,"bill_no": bill_no, 'optime':optime,
                           'change_amount': change_amount,'change_total_amount':change_total_amount, 'change_fund': change_fund,
                           'change_pay_amount': change_pay_amount
                           }
                obj = self.model(**oldData)
                self.db.add(obj)

            # 代付pending
            if water_type == 6:
                pending_amount = float(change_amount)
                change_pending_amount = float(obj.change_pending_amount) + float(change_amount)
                pay_amount = -float(change_amount)

                tmp_change_pay_amount = float(obj.change_pay_amount) - float(change_amount)
                change_pay_amount = Decimal(float(tmp_change_pay_amount)).quantize(Decimal("0.0000"))

                change_fund = obj.change_fund
                change_total_amount = obj.change_total_amount

                oldData = {"merchant_id": merchant_id, "water_type": water_type, "bill_no": bill_no, 'optime': optime,
                           'pending_amount': pending_amount, 'change_total_amount': change_total_amount,
                           'change_pending_amount': change_pending_amount,'pay_amount': pay_amount,'change_pay_amount':change_pay_amount,
                           'change_fund': change_fund}
                obj = self.model(**oldData)
                self.db.add(obj)

            # 代付成功
            if water_type == 7:
                pending_amount = -float(change_amount)

                tmp_change_pending_amount = float(obj.change_pending_amount) - float(change_amount)
                change_pending_amount = Decimal(float(tmp_change_pending_amount)).quantize(Decimal("0.0000"))

                change_pay_amount = obj.change_pay_amount
                change_fund = obj.change_fund

                tmp_change_total_amount = float(change_pending_amount) + float(change_pay_amount) + float(obj.change_fund)
                change_total_amount = Decimal(float(tmp_change_total_amount)).quantize(Decimal("0.0000"))

                oldData = {"merchant_id": merchant_id, "water_type": water_type, "bill_no": bill_no, 'optime': optime,
                           'pending_amount': pending_amount, 'change_total_amount': change_total_amount,
                           'change_pending_amount': change_pending_amount, 'change_pay_amount':change_pay_amount,
                           'change_fund': change_fund}
                obj = self.model(**oldData)
                self.db.add(obj)

            # 代付失败
            if water_type == 8:
                pending_amount = f"-{change_amount}"
                pay_amount = change_amount

                tmp_change_pending_amount = float(obj.change_pending_amount) - float(change_amount)
                change_pending_amount = Decimal(float(tmp_change_pending_amount)).quantize(Decimal("0.0000"))

                tmp_change_pay_amount = float(obj.change_pay_amount) + float(change_amount)
                change_pay_amount = Decimal(float(tmp_change_pay_amount)).quantize(Decimal("0.0000"))

                change_total_amount = obj.change_total_amount
                change_fund = obj.change_fund

                oldData = {"merchant_id": merchant_id, "water_type": water_type, "bill_no": bill_no,'optime': optime,
                           'pending_amount': pending_amount, 'change_total_amount': change_total_amount,
                           'change_pending_amount': change_pending_amount, 'change_pay_amount': change_pay_amount,
                           'pay_amount': pay_amount, 'change_fund': change_fund}
                obj = self.model(**oldData)
                self.db.add(obj)



        else:
            #没有数据直接插入
            if water_type == 4:
                change_amount = Decimal(float(change_amount)).quantize(Decimal("0.0000"))
                newData = {"merchant_id": merchant_id, "water_type": water_type,"bill_no": bill_no, 'optime':optime,
                           'change_amount': change_amount,'change_total_amount':change_amount, 'change_fund': change_amount}
                insert_stmt = insert(self.model).values(**newData)
                on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(**newData)
                await self.db.execute(on_duplicate_key_stmt)



            # 修改账号金额为0也可以上分
            if water_type == 1:
                tmp_change_fund =  float(change_amount)
                change_fund = Decimal(float(tmp_change_fund)).quantize(Decimal("0.0000"))
                tmp_change_total_amount =  float(change_amount)
                change_total_amount = Decimal(float(tmp_change_total_amount)).quantize(Decimal("0.0000"))

                oldData = {"merchant_id": merchant_id, "water_type": water_type, "bill_no": bill_no, 'optime': optime,
                           'change_amount': change_amount, 'change_total_amount': change_total_amount,
                           'change_fund': change_fund
                           }
                obj = self.model(**oldData)
                self.db.add(obj)

        await self.db.flush()
