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
from ...vadmin.auth.utils.current import FullAdminAuth
from ...vadmin.auth.utils.validation import Auth


app = APIRouter()


# 获取按钮列表
@app.get("/getbtnList", summary="获取按钮列表")
async def getBtnListDal(auth: Auth = Depends(FullAdminAuth())):
    datas = await crud.BankWaterDal(auth.db).get_datas()
    return SuccessResponse(datas)

# 根据id获取
@app.get("/getBtnById/{data_id}", summary="根据id获取")
async def getChannelByIdDal(data_id: int, auth: Auth = Depends(FullAdminAuth())):
    schema = schemas.BankWaterSchemasOut
    return SuccessResponse(await crud.BankWaterDal(auth.db).get_data(data_id, v_schema=schema))


# 获取options
# @app.get("/btnOptions", summary="获取options")
# async def get_btn_options(auth: Auth = Depends(FullAdminAuth())):
#     return SuccessResponse(await crud.BankWaterDal(auth.db).get_select_datas())


# 添加上传银行流水按钮
@app.post("/createbtn", summary="添加上传银行流水按钮")
async def createButtonDal(data: schemas.BankWaterSchemasIn, auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.BankWaterDal(auth.db).create_data(data))



# 编辑
@app.put("/editbtn/{data_id}", summary="编辑")
async def updateBtnById(data_id: int, data: schemas.BankWaterSchemasIn, auth: Auth = Depends(FullAdminAuth())):
    schema = schemas.BankWaterSchemasOut
    return SuccessResponse(await crud.BankWaterDal(auth.db).put_data(data_id, data, v_schema=schema))


# 删除通道/批量删除
@app.delete("/removebtn", summary="删除通道")
async def removeChannelByIds(ids: IdList = Depends(), auth: Auth = Depends(FullAdminAuth())):
    await crud.BankWaterDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")