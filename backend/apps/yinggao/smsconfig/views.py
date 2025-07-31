#!/usr/bin/python
# -*- coding: utf-8 -*-
# @author         : xhw
# @version        : 1.0
# @Create Time    : 2024/11/22
# @File           : view.py
# @IDE            : PyCharm
# @python         : 3.10+
# @fastapi        : 0.110.0
# @filename       : 短信列表

from fastapi import APIRouter, Depends

from utils.response import SuccessResponse
from . import schemas, crud
from .params import SmsParams
from ...vadmin.auth.utils.current import FullAdminAuth
from ...vadmin.auth.utils.validation import Auth
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import db_getter

app = APIRouter()


# 添加短信
@app.post("/createSms", summary="添加短信")
async def createSmsDal(data: dict, db: AsyncSession = Depends(db_getter)):
    return SuccessResponse(await crud.SmsPostDal(db).addSmsData(data))



# 根据短信ID查询是否存在
@app.get("/getSmsId/{sms_id}", summary="根据短信ID查询是否存在")
async def getSmsIdDal(sms_id: int, db: AsyncSession = Depends(db_getter)):
    return SuccessResponse(await crud.SmsPostDal(db).getSmsIdData(sms_id))



# 获取短信列表
@app.get("/getSmsList", summary="获取短信列表")
async def getSmsListDal(params: SmsParams = Depends(),auth: Auth = Depends(FullAdminAuth())):
    datas, count = await crud.SmsDal(auth.db).get_datas(**params.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)

