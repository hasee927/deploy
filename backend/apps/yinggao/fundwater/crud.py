from sqlalchemy.ext.asyncio import AsyncSession
from core.crud import DalBase
from core.exception import CustomException
from utils.checkSign import verificationSign
from . import models, schemas
from sqlalchemy import select, func
from utils.excel.excel_manage import ExcelManage
from ..collectionorder.help import get_merchant_key, merchant_white_ip
from fastapi.encoders import jsonable_encoder


class FundWaterDal(DalBase):
    def __init__(self, db: AsyncSession):
        super(FundWaterDal, self).__init__()
        self.db = db
        self.model = models.FundWater
        self.schema = schemas.FundWaterSchemasOut



    # 获取流水列表
    async def get_fundwater_datas(self,page: int = 1,limit: int = 10,v_order: str = None,v_order_field: str = None,**kwargs):
        # page: 1
        # limit: 10
        # channel_code: BOM190
        # from_date: 2025-04-11 00:00:00
        # to_date: 2025-04-11 17:36:48
        from_date = ''
        to_date = ''
        sql = select(self.model)

        # 条件查询
        conditions = []
        for field, value in kwargs.items():
            if field == "from_date":
                from_date = value
            if field == "to_date":
                to_date = value

            if field != 'from_date' and field != 'to_date' and value:
                attr = getattr(self.model, field)
                conditions.append(attr.like(f"%{value}%"))

        sql = sql.where(*conditions)

        if from_date and to_date:
            sql = sql.where(self.model.create_datetime.between(from_date, to_date))

        # 获取数据总数
        count_sql = select(func.count()).select_from(sql.alias())
        count_queryset = await self.db.execute(count_sql)
        count = count_queryset.one()[0]

        if limit != 0:
            # order_by(self.model.id.desc()) 按id倒序
            sql = sql.offset((page - 1) * limit).limit(limit).order_by(self.model.id.desc())

        queryset = await self.db.scalars(sql)

        result = queryset.unique().all()
        datas = [await self.out_dict(i) for i in result]
        return datas, count


    # 根据商户ID获取商户资金
    async def merchant_fund(self, request, params, rd):
        # 判断ip is white List
        await merchant_white_ip(request, params.merchant_id, rd, self.db)

        # 0, 获取商户key
        api_key = await get_merchant_key(params.merchant_id, rd, self.db)
        if not api_key:
            raise CustomException("api_key不存在!", code=400)

        # 校验签名
        signStr = (f"merchant_id={params.merchant_id}")
        verificationSign(signStr, api_key, params.sign, '')

        sql = select(self.model).where(self.model.merchant_id == params.merchant_id).order_by(self.model.id.desc()).limit(1)
        obj = await self.db.scalar(sql)

        if obj:
            data = {
                "merchant_id": obj.merchant_id,
                "payInAmount": obj.change_fund,  # 代收余额
                "payOutAmount": obj.change_pay_amount #代付余额
            }
            return jsonable_encoder(data)

    # 导出查询列表为excel
    async def export_excel(self, data: any):
        # 获取表头
        row = ['流水号', '商户ID', '流水类型', '所属单号', '变动余额', '在途金额变动', '代付金额变动', '变动后总金额', '变动后在途金额', '变动后代付金额', '变动后可转换金额', '操作时间', '备注']
        rows = []
        from_date = ''
        to_date = ''
        sql = select(self.model)

        if data:
            # 条件查询
            conditions = []
            for field, value in data.items():
                if field == "from_date":
                    from_date = value
                if field == "to_date":
                    to_date = value

                if field != 'from_date' and field != 'to_date' and value:
                    attr = getattr(self.model, field)
                    conditions.append(attr.like(f"%{value}%"))

            sql = sql.where(*conditions)

            if from_date and to_date:
                sql = sql.where(self.model.optime.between(from_date, to_date))


        queryset = await self.db.scalars(sql)
        result = queryset.unique().all()
        for item in result:
            rows.append([item.id, item.merchant_id, item.water_type, item.bill_no, item.change_amount, item.pending_amount,
                         item.pay_amount, item.change_total_amount, item.change_pending_amount, item.change_pay_amount, item.change_fund,
                         str(item.optime), item.remark])

        em = ExcelManage()
        em.create_excel("资金流水")
        em.write_list(rows, row)
        remote_file_url = em.save_excel().get("remote_path")
        em.close()
        return {"url": remote_file_url, "filename": "资金流水.xlsx"}



