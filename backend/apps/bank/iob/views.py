from fastapi import APIRouter, Depends
from core.dependencies import IdList
from utils.response import SuccessResponse, ErrorResponse
from apps.bank.iob.params.iob import IobParams
from apps.vadmin.auth.utils.current import  FullAdminAuth
from apps.vadmin.auth.utils.validation.auth import Auth
from . import schemas, crud
# from .crud import getIobData

app = APIRouter()

# 获取IOB用户列表
@app.get("/getioblist", summary="获取IOB用户列表")
async def getIob(
        params: IobParams = Depends(),
        auth: Auth = Depends(FullAdminAuth())
):
    datas, count = await crud.IobDal(auth.db).get_datas(**params.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)

# 根据id获取IOB用户
@app.get("/getIobById/{data_id}", summary="根据id获取IOB用户")
async def getIobById(data_id: int, auth: Auth = Depends(FullAdminAuth())):
    schema = schemas.IobSchemasOut
    return SuccessResponse(await crud.IobDal(auth.db).get_data(data_id, v_schema=schema))


# 创建iob用户
@app.post("/addiobuser", summary="创建iob用户")
async def getIobById(data: schemas.IobSchemasIn, auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.IobDal(auth.db).create_data(data=data))


# 编辑iob用户
@app.put("/editiobuser/{data_id}", summary="创建iob用户")
async def getIobById(data_id: int, data: schemas.IobSchemasIn, auth: Auth = Depends(FullAdminAuth())):
    schema = schemas.IobSchemasOut
    return SuccessResponse(await crud.IobDal(auth.db).put_data(data_id, data, v_schema=schema))


# 删除iob用户
@app.delete("/deliobuser", summary="删除iob用户")
async def getIobById(ids: IdList = Depends(), auth: Auth = Depends(FullAdminAuth())):
    await crud.IobDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


# @app.get("/getdetail", summary="测试接口获取数据")
# async def getData():
#     myInstance = getIobData()
#     dataObj = await myInstance.getListData()
#     print(dataObj)
#     return dataObj