from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr

class BankWaterSchemasIn(BaseModel):
    name: str
    desc: str
    image: str | None = None


class BankWaterSchemasOut(BankWaterSchemasIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr


class BankWaterOptions(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str