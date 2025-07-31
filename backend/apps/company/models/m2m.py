#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/7/7 13:41
# @File           : m2m.py
# @IDE            : PyCharm
# @desc           : 关联中间表

from db.db_base import Base
from sqlalchemy import ForeignKey, Column, Table, Integer


company_person_job = Table(
    "company_person_job",
    Base.metadata,
    Column("person_id", Integer, ForeignKey("company_person.id", ondelete="CASCADE")),
    Column("job_id", Integer, ForeignKey("company_job.id", ondelete="CASCADE")),
)
