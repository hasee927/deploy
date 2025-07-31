from typing import Annotated, List


from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, Table, Column
from db.db_base import BaseModel , Base
from sqlalchemy import String, Boolean, Integer
import datetime
from .m2m import company_person_job



required_unique_string = Annotated[str, mapped_column(String(128), unique=True, nullable=False)]
timestamp_not_null = Annotated[datetime.datetime, mapped_column(nullable=False)]


class Department(BaseModel):
    __tablename__ = "department"
    name: Mapped[required_unique_string]
    employees: Mapped[List["Employee"]] = relationship(back_populates="department")

    def __repr__(self):
        return f'id: {self.id}, name: {self.name}'


class Employee(BaseModel):
    __tablename__ = "employee"

    dept_id: Mapped[int] = mapped_column(Integer, ForeignKey("department.id"), comment="部门")
    name: Mapped[required_unique_string]
    birthday: Mapped[timestamp_not_null]

    department: Mapped[Department] = relationship(back_populates="employees")

    def __repr__(self):
        return f'id: {self.id}, dept_id: {self.dept_id}, name: {self.name}, birthday: {self.birthday}'

########################## many to many #################################################

# company_person_job = Table(
#     "company_person_job",
#     Base.metadata,
#     Column("person_id", Integer, ForeignKey("company_person.id", ondelete="CASCADE")),
#     Column("job_id", Integer, ForeignKey("company_job.id", ondelete="CASCADE")),
# )



class companyJob(BaseModel):
    __tablename__ = "company_job"
    name: Mapped[required_unique_string]
    introduce: Mapped[required_unique_string] = mapped_column(comment="工作技能")

    # person: Mapped[set["companyPerson"]] = relationship(secondary=company_person_job)

    def __repr__(self):
        return f'id: {self.id}, name: {self.name}, introduce: {self.introduce}'



class companyPerson(BaseModel):
    __tablename__ = "company_person"

    name: Mapped[required_unique_string]
    age: Mapped[int]

    job: Mapped[set["companyJob"]] = relationship(secondary=company_person_job)

    def __repr__(self):
        return f'name: {self.name}, age: {self.age}'


