from fastapi import APIRouter, Depends
from utils.response import SuccessResponse
from . import schemas, crud
from apps.vadmin.auth.utils.current import FullAdminAuth
from .params import DeptParams
from .schemas import PersonSchemasIn
from ..vadmin.auth.utils.validation import Auth
from core.dependencies import IdList

app = APIRouter()


# 添加部门名称
@app.post("/newAddDept", summary="添加部门名称")
async def newAddDept(data: schemas.DeptSchemasIn, auth: Auth = Depends(FullAdminAuth())):
    res = crud.DeptData(auth.db, data).addDept()
    return SuccessResponse(await res)


# 获取部门名称分页列表
@app.get("/getDeptPages", summary="获取部门名称分页列表")
async def getEmpDataById(params: DeptParams = Depends(), auth: Auth = Depends(FullAdminAuth())):
    res, count = await crud.DeptData(auth.db).getDataPage(**params.dict())
    return SuccessResponse(res, count=count)



# 根据id获取部门名称
@app.get("/getDeptById/{data_id}", summary="根据id获取部门名称")
async def getEmpDataById(data_id: int, auth: Auth = Depends(FullAdminAuth())):
    res = crud.DeptData(auth.db).getDeptById(data_id)
    return SuccessResponse(await res)


#############################################################################################
#############################################################################################
#############################################################################################


# 添加员工名称
@app.post("/newAddEmp", summary="添加员工名称")
async def newAddDept(data: schemas.EmpSchemasIn, auth: Auth = Depends(FullAdminAuth())):
    res = crud.EmpData(auth.db, data).addEmp()
    return SuccessResponse(await res)


# 根据id获取员工信息
@app.get("/getEmpById/{data_id}", summary="根据id获取员工信息")
async def getEmpDataById(data_id: int, auth: Auth = Depends(FullAdminAuth())):
    res = crud.EmpData(auth.db).getEmpById(data_id)
    return SuccessResponse(await res)


########################## many to many #################################################

# 根据id获取个人信息
@app.get("/getPersonById/{data_id}", summary="根据id获取个人信息")
async def getPersonDataById(data_id: int, auth: Auth = Depends(FullAdminAuth())):
    res = crud.PersonData(auth.db).getPersonById(data_id)
    return SuccessResponse(await res)


# 添加个人信息
@app.post("/createPerson", summary="添加个人信息")
async def getPersonDataById(data: PersonSchemasIn, auth: Auth = Depends(FullAdminAuth())):
    res = crud.PersonData(auth.db, data).createPerson()
    return SuccessResponse(await res)


# 根据id修改个人信息
@app.put("/editPersonById/{data_id}", summary="根据id修改个人信息")
async def editPersonDataById(data_id: int,data: PersonSchemasIn ,auth: Auth = Depends(FullAdminAuth())):
    res = crud.PersonData(auth.db, data).editPersonById(data_id)
    return SuccessResponse(await res)


# 根据id批量删除个人信息
@app.delete("/removePersonByIds", summary="根据id批量删除个人信息")
async def removePersonDataById(ids: IdList = Depends() ,auth: Auth = Depends(FullAdminAuth())):
    res = crud.PersonData(auth.db).removePersonById(ids=ids.ids)
    return SuccessResponse(await res)




# 根据id获取工作信息
@app.get("/getJobById/{data_id}", summary="根据id获取工作信息")
async def getJobDataById(data_id: int, auth: Auth = Depends(FullAdminAuth())):
    res = crud.JobData(auth.db).getJobById(data_id)
    return SuccessResponse(await res)








