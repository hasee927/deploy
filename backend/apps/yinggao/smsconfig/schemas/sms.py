from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr

class SmsSchemasIn(BaseModel):
    channel_code: str
    context: str | None = None


class SmsSchemasOut(SmsSchemasIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr

    sender_addr: str | None = None
    sms_time: str | None = None
    sms_type: str | None = None
    code: str | None = None
    sms_id: str | None = None
    sms_utc_time: str | None = None

