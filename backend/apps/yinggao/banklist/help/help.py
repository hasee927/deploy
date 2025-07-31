from sqlalchemy.ext.asyncio import AsyncSession

from .upload_equ import equ
from .upload_idbi import idbi
from .upload_indian import indian
from .upload_psb import psb
from .upload_rbl import rbl
from .upload_sdb import sdb
from ..import models, schemas
from .upload_iob import iob
from .upload_bom import bom
from .upload_cab import cab
from .upload_pfed import pfed


class upload_data:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.model = models.Banklist
        self.schema = schemas.BKListSchemasOut


    async def import_csv_data(self, data):
        res = ""

        if data.bank_name == "iob":
            res = await iob(data, self.db)
        if data.bank_name == "pbom":
            res = await bom(data, self.db)
        if data.bank_name == "cab":
            res = await cab(data, self.db)
        if data.bank_name == "pfed":
            res = await pfed(data, self.db)
        if data.bank_name == "idbi":
            res = await idbi(data, self.db)
        if data.bank_name == "psb":
            res = await psb(data, self.db)
        if data.bank_name == "sdb":
            res = await sdb(data, self.db)
        if data.bank_name == "indian":
            res = await indian(data, self.db)
        if data.bank_name == "equ":
            res = await equ(data, self.db)
        if data.bank_name == "rbl":
            res = await rbl(data, self.db)

        return res


