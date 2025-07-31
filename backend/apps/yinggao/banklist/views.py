#!/usr/bin/python
# -*- coding: utf-8 -*-
# @author         : xhw
# @version        : 1.0
# @Create Time    : 2024/11/22
# @File           : view.py
# @IDE            : PyCharm
# @python         : 3.10+
# @fastapi        : 0.110.0
# @filename       : 银行列表


from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import db_getter, redis_getter
from utils.response import SuccessResponse
from . import schemas, crud
from .params import BankListParams
from ...vadmin.auth.utils.current import FullAdminAuth
from ...vadmin.auth.utils.validation import Auth
from fastapi import File, UploadFile
from redis.asyncio import Redis


app = APIRouter()


# 获取银行列表
@app.get("/getBKList", summary="获取银行列表")
async def getBKListDal(params: BankListParams = Depends(),auth: Auth = Depends(FullAdminAuth())):
    datas, count = await crud.BKListDal(auth.db).get_datas(**params.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)

# 收银台获取utr， 校验银行流水判断utr是否存在，如存在则支付成功
@app.get("/getutr", summary="获取utr")
async def getUtrDal(params: BankListParams = Depends(),db: AsyncSession = Depends(db_getter)):
    datas = await crud.BKListDal(db).get_datas(**params.dict())
    return SuccessResponse(datas)



# 添加银行列表数据---对外提供接口---不需要token验证。实例化db: AsyncSession = Depends(db_getter)无需token认证
@app.post("/createbklistdata", summary="添加银行列表数据")
async def createBKListDal(data: list[dict], db: AsyncSession = Depends(db_getter)):
    return SuccessResponse(await crud.BKListPostDal(db).addBKListData(data))



# 接收上传文件----暂时没有登录认证
@app.post("/uploadfile", summary="接收上传文件")
async def uploadFileCsvDal(file: UploadFile = File(...), db: AsyncSession = Depends(db_getter)):
    datas = await crud.BKListDal(db).uploadCsvFile(file)
    return SuccessResponse(datas)



# 手动导入数据
@app.post("/importcsv", summary="手动导入数据")
# async def importCsvDal(data: schemas.BKListSchemasIn, auth: Auth = Depends(FullAdminAuth())):
async def importCsvDal(data: schemas.BKListSchemasIn, db: AsyncSession = Depends(db_getter)):
    res = await crud.BKListDal(db).importCsvFile(data)
    return SuccessResponse(res)


##############################处理idbi手动输入验证码###################################################
##############################处理idbi手动输入验证码###################################################
# # 1，接收上传验证码图片
# @app.post("/uploadCaptcha", summary="接收上传验证码")
# async def uploadImageDal(file: UploadFile = File(...), db: AsyncSession = Depends(db_getter)):
#     datas = await crud.BKListDal(db).uploadCaptcha(file)
#     return SuccessResponse(datas)
#
#
# # 2，接收前端手动输入的验证码
# @app.post("/manualCaptcha", summary="获取验证码")
# async def manualCaptchaDal(data: dict, auth: Auth = Depends(FullAdminAuth())):
#     datas = await crud.BKListDal(auth.db).manualCaptchaImageData(data)
#     return SuccessResponse(datas)
#
#
# # 3，进入银行系统后清空验证码
# @app.get("/removeCaptcha", summary="进入银行系统后清空验证码")
# async def removeCaptchaDal(db: AsyncSession = Depends(db_getter)):
#     res = await crud.BKListDal(db).removeCaptchaImageData()
#     return SuccessResponse(res)
#
#
#
# # 4，监听redis验证码错误消息
# @app.get("/listenErrorMsg", summary="监听redis验证码错误消息")
# async def listenErrorMsgDal(data: str, db: AsyncSession = Depends(db_getter), rd: Redis = Depends(redis_getter)):
#     res = await crud.BKListDal(db).listenErrorMsgData(data, rd)
#     return SuccessResponse(res)


##############################处理idbi手动输入验证码###################################################
##############################处理idbi手动输入验证码###################################################