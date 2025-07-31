from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr

class SuccessOrderSchemasIn(BaseModel):
    bank_name: str | None = None #银行名称
    channel_code: str | None = None #通道code
    success_order: int | None = None #成功订单数
    fail_order: int | None = None #失败订单数
    total_order: int | None = None #总订单数
    success_rate: str | None = None #成功率"
    success_amount: str | None = None #成功订单金额
    total_amount: str | None = None #订单总金额


class SuccessOrderSchemasOut(SuccessOrderSchemasIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr