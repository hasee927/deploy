from fastapi import Depends
import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.strategy_options import _AbstractLoad, contains_eager
from apps.bank.iob.models import Bank_Iob
from sqlalchemy import select, create_engine
from typing import *
from core.crud import DalBase
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas

class IobDal(DalBase):
    def __init__(self, db: AsyncSession):
        super(IobDal, self).__init__()
        self.db = db
        self.model = models.Bank_Iob
        self.schema = schemas.IobSchemasOut

