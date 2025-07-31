from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr



#部门
class DeptSchemasIn(BaseModel):
    name: str


class DeptSchemasOut(DeptSchemasIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr

#员工
class EmpSchemasIn(BaseModel):
    name: str
    birthday: str | None = None
    dept_id: int


class EmpSchemasOut(EmpSchemasIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr



#个人
class PersonSchemasIn(BaseModel):
    name: str
    age: int
    job_ids: list[int] = []


class PersonSchemasOut(PersonSchemasIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr


#工作
class JobSchemasIn(BaseModel):
    name: str
    introduce: str

class JobSchemasOut(JobSchemasIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr






















