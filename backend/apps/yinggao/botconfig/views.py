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
from core.dependencies import IdList
from utils.response import SuccessResponse
from . import schemas, crud
from .params import BotParams
from ...vadmin.auth.utils.current import FullAdminAuth
from ...vadmin.auth.utils.validation import Auth
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import db_getter

app = APIRouter()

# 获取机器人列表
@app.get("/getBotList", summary="获取机器人列表")
async def getBotListDal(params: BotParams = Depends(),auth: Auth = Depends(FullAdminAuth())):
    datas, count = await crud.BotDal(auth.db).get_datas(**params.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)


# 添加机器人
@app.post("/addBot", summary="添加机器人")
async def createBotDal(data: schemas.BotSchemasIn,auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.BotDal(auth.db).create_data(data=data))


# 根据id获取机器人
@app.get("/getBotById/{data_id}", summary="根据id获取机器人")
async def getBotByIdDal(data_id: int, auth: Auth = Depends(FullAdminAuth())):
    schema = schemas.BotSchemasOut
    return SuccessResponse(await crud.BotDal(auth.db).get_data(data_id, v_schema=schema))


# 编辑机器人
@app.put("/editBot/{data_id}", summary="编辑机器人")
async def editBotById(data_id: int, data: schemas.BotSchemasIn, auth: Auth = Depends(FullAdminAuth())):
    schema = schemas.BotSchemasOut
    return SuccessResponse(await crud.BotDal(auth.db).put_data(data_id, data, v_schema=schema))


# 批量删除
@app.delete("/removeBot", summary="删除机器人")
async def removeBotByIds(ids: IdList = Depends(), auth: Auth = Depends(FullAdminAuth())):
    await crud.BotDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


# 群发消息
@app.post("/sendmsg", summary="群发消息")
async def senderMsgDal(data: dict,auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.BotDal(auth.db).senderMsg(data=data))
