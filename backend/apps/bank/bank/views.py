from fastapi import APIRouter, Depends

from utils.response import SuccessResponse
from . import schemas, crud
from .params import BankParams
from ...vadmin.auth.utils.current import FullAdminAuth
from ...vadmin.auth.utils.validation import Auth

app = APIRouter()


# 添加银行数据
@app.post("/addBank", summary="添加银行数据")
async def addBankData(data: schemas.BankSchemasIn, auth: Auth = Depends(FullAdminAuth())):
    res = crud.BankData(auth.db, data).addBank()
    return SuccessResponse(await res)


# 获取银行数据列表
@app.get("/getBanks", summary="获取银行数据列表")
async def getBankData(auth: Auth = Depends(FullAdminAuth())):
    res = crud.BankData(auth.db).getBanks()
    return SuccessResponse(await res)


# 获取银行分页数据
@app.get("/getBanksPages", summary="获取银行分页数据")
async def getBankDataPage(params: BankParams = Depends(), auth: Auth = Depends(FullAdminAuth())):
    res, count = await crud.BankData(auth.db).getDataPage(**params.dict())
    return SuccessResponse(res, count=count)


# 根据id获取银行数据
@app.get("/getBankById/{data_id}", summary="根据id获取银行数据")
async def getBankData(data_id: int, auth: Auth = Depends(FullAdminAuth())):
    res = crud.BankData(auth.db).getBankById(data_id)
    return SuccessResponse(await res)


# 根据id编辑银行数据
@app.put("/editBankById/{data_id}", summary="根据id编辑银行数据")
async def editBankData(data_id: int, data: schemas.BankSchemasIn,  auth: Auth = Depends(FullAdminAuth())):
    res = crud.BankData(auth.db).editBankById(data_id, data)
    return SuccessResponse(await res)


# 根据id删除银行数据
@app.delete("/delBankById/{data_id}", summary="根据id删除银行数据")
async def editBankData(data_id: int,  auth: Auth = Depends(FullAdminAuth())):
    res = crud.BankData(auth.db).delBankById(data_id)
    return SuccessResponse(await res)