from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr

class BankSchemasIn(BaseModel):
    name: str
    addr: str | None = None
    phone: str | None = None
    desc: str | None = None


class BankSchemasOut(BankSchemasIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr