#!/usr/bin/python
# -*- coding: utf-8 -*-
# @author         : xhw
# @version        : 1.0
# @Create Time    : 2024/11/22
# @File           : view.py
# @IDE            : PyCharm
# @python         : 3.10+
# @fastapi        : 0.110.0
# @filename       : 商户列表

from fastapi import APIRouter, Depends
from utils.response import SuccessResponse
from . import schemas, crud
from .params import FinanceParams
from ...vadmin.auth.utils.current import FullAdminAuth
from ...vadmin.auth.utils.validation import Auth

app = APIRouter()


# 获取商户资金列表
@app.get("/getFinanceList", summary="获取商户资金列表")
async def getFinanceDal(params: FinanceParams = Depends(),auth: Auth = Depends(FullAdminAuth())):
    res, count = await crud.FinanceDal(auth.db).getFinanceData(**params.dict())
    return SuccessResponse(res, count=count)


# 根据id获取商户资金
@app.get("/getFinanceById/{data_id}", summary="根据id获取商户资金")
async def getFinanceByIdDal(data_id: int, auth: Auth = Depends(FullAdminAuth())):
    schema = schemas.FinanaceSchemasOut
    return SuccessResponse(await crud.FinanceDal(auth.db).get_data(data_id, v_schema=schema))


# 调账
@app.put("/editFinance/{data_id}", summary="编辑通道")
async def updateFinanceById(data_id: int, data: schemas.FinanaceSchemasIn, auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.FinanceDal(auth.db).update_finance_data(data_id, data))