#!/usr/bin/python
# -*- coding: utf-8 -*-
# @author         : xhw
# @version        : 1.0
# @Create Time    : 2024/11/22
# @File           : view.py
# @IDE            : PyCharm
# @python         : 3.10+
# @fastapi        : 0.110.0
# @filename       : 通道列表

from fastapi import APIRouter, Depends
from redis.asyncio import Redis
from core.dependencies import IdList
from utils.response import SuccessResponse
from . import schemas, crud
from .params import ChannelParams
from ...vadmin.auth.utils.current import FullAdminAuth
from ...vadmin.auth.utils.validation import Auth
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import db_getter, redis_getter



app = APIRouter()


# 添加通道
@app.post("/createChannel", summary="添加通道")
async def createChannelDal(data: schemas.ChannelSchemasIn,auth: Auth = Depends(FullAdminAuth(permissions=["merchant.channel.create"]))):
    return SuccessResponse(await crud.ChannelDal(auth.db).create_data(data=data))


# 获取通道列表
@app.get("/getChannelList", summary="获取通道列表")
async def getChannelListDal(params: ChannelParams = Depends(),auth: Auth = Depends(FullAdminAuth())):
    datas, count = await crud.ChannelDal(auth.db).get_datas(**params.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)

# 获取大额代收通道选择项
@app.get("/bigInOptions", summary="获取大额代收通道选择项")
async def get_big_in_channel_options(auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.ChannelDal(auth.db).get_large_in_select_datas())






# 获取大额代付通道选择项
@app.get("/bigPayOptions", summary="获取大额代付通道选择项")
async def get_big_pay_channel_options(auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.ChannelDal(auth.db).get_big_pay_select_datas())





# 根据id获取通道
@app.get("/getChannelById/{data_id}", summary="根据id获取通道")
async def getChannelByIdDal(data_id: int, auth: Auth = Depends(FullAdminAuth())):
    schema = schemas.ChannelSchemasOut
    return SuccessResponse(await crud.ChannelDal(auth.db).get_data(data_id, v_schema=schema))


# 编辑通道
@app.put("/editChannel/{data_id}", summary="编辑通道")
async def updateChannelById(data_id: int, data: schemas.ChannelSchemasIn, auth: Auth = Depends(FullAdminAuth(permissions=["merchant.channel.update"]))):
    schema = schemas.ChannelSchemasOut
    return SuccessResponse(await crud.ChannelDal(auth.db).put_data(data_id, data, v_schema=schema))


# 删除通道/批量删除
@app.delete("/removeChannel", summary="删除通道")
async def removeChannelByIds(ids: IdList = Depends(), auth: Auth = Depends(FullAdminAuth(permissions=["merchant.channel.delete"]))):
    await crud.ChannelDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


# 获取在线的通道列表
@app.get("/online/{sign}", summary="获取在线的通道列表")
async def get_online_channel(sign: str ,db: AsyncSession = Depends(db_getter)):
    return SuccessResponse(await crud.ChannelDal(db).get_Online_ChannelCode(sign))


# 上报通道是否在线
@app.get("/checkstatus", summary="上报通道是否在线")
async def get_checkstatus_channel(code: str, status: str, db: AsyncSession = Depends(db_getter), rd: Redis = Depends(redis_getter)):
    return SuccessResponse(await crud.ChannelDal(db).get_Status_ChannelCode(code, status, rd))
