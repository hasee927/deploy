from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr

class ChannelSchemasIn(BaseModel):
    pay_company: str
    name: str | None = None
    channel_code: str
    channel_name: str
    channel_type: int
    channel_status: int
    pay_gw_addr: str | None = None #"支付网关地址"
    pay_gw_check_status_addr: str | None = None #"状态检查地址"
    pay_gw_merchant_id: str | None = None #代付网关商户名称(ID)
    pay_gw_id: str | None = None #"支付网关Id"
    pay_gw_token: str | None = None #"支付网关token"
    pay_gw_callback_id: str | None = None #"支付网关回调地址id"
    pay_gw_spare: str | None = None #"支付网关备用字段"

    remark: str | None = None


class ChannelSchemasOut(ChannelSchemasIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr


class ChannelOptionsOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    label: str = Field(alias='channel_code')
    value: int = Field(alias='id')

