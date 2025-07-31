#!/usr/bin/python
# -*- coding: utf-8 -*-
# @author         : xhw
# @version        : 1.0
# @Create Time    : 2025/02/12
# @File           : view.py
# @IDE            : PyCharm
# @python         : 3.10+
# @fastapi        : 0.110.0
# @filename       : 成功订单
# https://yanh.tech/2023/08/register-telegram-bot-and-build-a-bot-using-python/


from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import db_getter
from utils.response import SuccessResponse
from . import crud
from .params import SuccessOrderParams
from ...vadmin.auth.utils.current import FullAdminAuth
from ...vadmin.auth.utils.validation import Auth

app = APIRouter()


# 统计成功订单
@app.get("/success", summary="统计成功订单")
async def SuccessOrderDal(params: SuccessOrderParams = Depends(),auth: Auth = Depends(FullAdminAuth())):
    datas, count = await crud.SuccessOrderDal(auth.db).get_datas(**params.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)


# 机器人获取成功订单-每10分钟
@app.get("/botsuccess/{min}/{sign}", summary="机器人获取成功订单")
async def BotSuccessOrderDal(min: int, sign: str,db: AsyncSession = Depends(db_getter)):
    datas = await crud.SuccessOrderDal(db).getBotSuccessOrder(min, sign)
    return SuccessResponse(datas)


# 今日代收统计
@app.get("/todaycollection", summary="今日代收统计")
async def todayCollectionDal(auth: Auth = Depends(FullAdminAuth())):
    datas = await crud.SuccessOrderDal(auth.db).get_today_collection()
    return SuccessResponse(datas)


# 代收排行榜
@app.get("/collectionranking", summary="代收排行榜")
async def collectionRankingDal(auth: Auth = Depends(FullAdminAuth())):
    datas, count = await crud.SuccessOrderDal(auth.db).get_collection_ranking()
    return SuccessResponse(datas, count=count)



# 今日代付统计
@app.get("/todaypayout", summary="今日代付统计")
async def todayPayOutDal(auth: Auth = Depends(FullAdminAuth())):
    datas = await crud.SuccessOrderDal(auth.db).get_today_payout()
    return SuccessResponse(datas)


# 代付排行榜
@app.get("/payoutranking", summary="代付排行榜")
async def payoutRankingDal(auth: Auth = Depends(FullAdminAuth())):
    datas, count = await crud.SuccessOrderDal(auth.db).get_payout_ranking()
    return SuccessResponse(datas, count=count)


# 统计代付pendding金额
@app.get("/paypending", summary="统计代付pendding金额")
async def payPendingDal(auth: Auth = Depends(FullAdminAuth())):
    datas = await crud.SuccessOrderDal(auth.db).get_paypending_data()
    return SuccessResponse(datas)