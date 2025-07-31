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


app = APIRouter()

# 获取群聊列表
@app.get("/getGroupList", summary="获取群聊列表")
async def getBotListDal(params: BotParams = Depends(),auth: Auth = Depends(FullAdminAuth())):
    datas, count = await crud.BotDal(auth.db).get_datas(**params.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)


# 添加群聊
@app.post("/addgroup", summary="添加群聊")
async def createBotDal(data: schemas.BotGroupSchemasIn,auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.BotDal(auth.db).create_data(data=data))


# 根据id获取群聊
@app.get("/getGroupById/{data_id}", summary="根据id获取群聊")
async def getBotByIdDal(data_id: int, auth: Auth = Depends(FullAdminAuth())):
    schema = schemas.BotGroupSchemasOut
    return SuccessResponse(await crud.BotDal(auth.db).get_data(data_id, v_schema=schema))


# 编辑群聊
@app.put("/editGroup/{data_id}", summary="编辑群聊")
async def editBotById(data_id: int, data: schemas.BotGroupSchemasIn, auth: Auth = Depends(FullAdminAuth())):
    schema = schemas.BotGroupSchemasOut
    return SuccessResponse(await crud.BotDal(auth.db).put_data(data_id, data, v_schema=schema))


# 批量删除
@app.delete("/removeGroup", summary="删除机器人")
async def removeBotByIds(ids: IdList = Depends(), auth: Auth = Depends(FullAdminAuth())):
    await crud.BotDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")

