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

from fastapi import APIRouter, Depends, Request
from utils.response import SuccessResponse
from . import schemas, crud
from .params import FundWaterParams
from .params.fundwater import SignFundWaterParams
from ...vadmin.auth.utils.current import FullAdminAuth
from ...vadmin.auth.utils.validation import Auth
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import db_getter, redis_getter
from redis.asyncio import Redis

app = APIRouter()


#获取流水列表
@app.get("/getfundwater", summary="获取流水列表")
async def FundWaterList(params: FundWaterParams = Depends(),auth: Auth = Depends(FullAdminAuth())):
    res, count = await crud.FundWaterDal(auth.db).get_fundwater_datas(**params.dict())
    return SuccessResponse(res, count=count)



# 根据商户ID获取商户资金
@app.get("/merchantfund", summary="根据商户ID获取商户资金")
async def getmerchantfundDal(request: Request, params: SignFundWaterParams = Depends(), db: AsyncSession = Depends(db_getter), rd: Redis = Depends(redis_getter)):
    return SuccessResponse(await crud.FundWaterDal(db).merchant_fund(request, params, rd))



# 导出查询列表为excel
@app.post("/exportexcel", summary="导出查询列表为excel")
async def exportExcelList(data: dict,auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.FundWaterDal(auth.db).export_excel(data))