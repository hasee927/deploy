from sqlalchemy.orm import selectinload, joinedload

from . import models, schemas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, create_engine, ScalarResult, func, or_, delete
from fastapi.encoders import jsonable_encoder

class DeptData:

    def __init__(self, db: AsyncSession, data: any = None):
        self.db = db
        self.data = data
        self.model = models.Department
        self.schema = schemas.DeptSchemasOut

    # 添加部门名称
    async def addDept(self):
        obj = self.model(**self.data.model_dump())
        self.db.add(obj)
        await self.db.commit()
        return "添加成功"

    # 获取部门名称分页列表
    async def getDataPage(
            self,
            page: int = 1,
            limit: int = 10,
            v_order: str = None,
            v_order_field: str = None,
            **kwargs
    ):

        sql = select(self.model)

        # 获取数据总数
        count_sql = select(func.count()).select_from(sql.alias())
        count_queryset = await self.db.execute(count_sql)
        count = count_queryset.one()[0]

        # 条件查询
        conditions = []
        for field, value in kwargs.items():
            attr = getattr(self.model, field)
            if value[0] == "like" and value[1]:
                conditions.append(attr.like(f"%{value[1]}%"))
        sql = sql.where(*conditions)

        if limit != 0:
            sql = sql.offset((page - 1) * limit).limit(limit)

        queryset = await self.db.scalars(sql)
        return jsonable_encoder(queryset.unique().all()), count


    # 根据id获取部门名称
    async def getDeptById(self, data_id: int):
        # ForeignKey反向查询
        sql = select(self.model).options(selectinload(self.model.employees)).where(self.model.id == data_id)
        result = await self.db.execute(sql)
        data = {}
        for row in result.scalars():
            data.update(jsonable_encoder(row))
            data["employees"] = jsonable_encoder(row.employees)
        return data

######################################################################################################

class EmpData:

    def __init__(self, db: AsyncSession, data: any = None):
        self.db = db
        self.data = data
        self.model = models.Employee
        self.deptmodel = models.Department
        self.schema = schemas.EmpSchemasOut

    async def addEmp(self):
        obj = self.model(**self.data.model_dump())
        self.db.add(obj)
        await self.db.commit()
        return "添加成功"


    async def getEmpById(self, data_id: int):
        # ForeignKey正向查询
        # sql = select(self.model, self.deptmodel).join(self.model.department).where(self.model.id == data_id)
        sql = select(self.model).options(joinedload(self.model.department)).where(self.model.id == data_id)
        res = await self.db.execute(sql)
        data = {}
        for row in res.scalars():
            data.update(jsonable_encoder(row))
            data["department"] = (jsonable_encoder(row.department))
        return data


########################## many to many #################################################

class PersonData:

    def __init__(self, db: AsyncSession, data: any = None):
        self.db = db
        self.data = data
        self.model = models.companyPerson
        self.schema = schemas.PersonSchemasOut

    # 根据id获取个人信息
    async def getPersonById(self, data_id: int):
            # many to many
            sql = select(self.model).options(joinedload(self.model.job)).where(self.model.id == data_id)
            # 第一种方式
            queryset = await self.db.execute(sql)
            datas = queryset.scalars().unique().all()
            # 第二种方式
            # queryset = await self.db.scalars(sql)
            # datas = queryset.unique().all()
            dataDict = {}
            for per in datas:
                dataDict.update(jsonable_encoder(per))
                dataDict["job"] = jsonable_encoder(per.job)

            return dataDict

    # 添加个人信息
    async def createPerson(self):
        obj = self.model(**self.data.model_dump(exclude={'job_ids'}))

        # 循环job_ids([1,2])根据id查出job表中的对象，然后添加到Person表中的job（多对多）字段
        if self.data.job_ids:
            job_obj_data = JobData(self.db)  # 实例化JobData类对象
            for job_id in self.data.job_ids:
                sql = select(job_obj_data.model).where(job_obj_data.model.id == job_id) #根据id查找job对象
                queryset = await self.db.scalar(sql)
                obj.job.add(queryset) # 添加到Person表中的job（多对多）字段

        self.db.add(obj)
        await self.db.commit()
        return "添加成功"

    # 根据id修改个人信息
    async def editPersonById(self, data_id: int):
        job_obj_data = JobData(self.db)  # 实例化JobData类对象
        data_dict = jsonable_encoder(self.data)
        sql = select(self.model).options(joinedload(self.model.job)).where(self.model.id == data_id)
        obj = await self.db.scalar(sql)
        for key, value in data_dict.items():
            if key == "job_ids":
                if value:
                    if obj.job:
                        obj.job.clear()

                    for job_id in value:
                        sql = select(job_obj_data.model).where(job_obj_data.model.id == job_id)  # 根据id查找job对象
                        queryset = await self.db.scalar(sql)
                        obj.job.add(queryset)  # 添加到Person表中的job（多对多）字段
            setattr(obj, key, value)

        return "编辑成功"

    # 根据id批量删除个人信息
    async def removePersonById(self, ids: list[int]):

        sqls = select(self.model).options(joinedload(self.model.job)).where(self.model.id.in_(ids))
        queryset = await self.db.scalars(sqls)
        for obj in queryset.unique().all():
            if obj.job:
                obj.job.clear()

        await self.db.execute(delete(self.model).where(self.model.id.in_(ids)))
        return "删除成功"


class JobData:

    def __init__(self, db: AsyncSession, data: any = None):
        self.db = db
        self.data = data
        self.model = models.companyJob
        self.schema = schemas.JobSchemasOut

    # 根据id获取工作信息
    async def getJobById(self, data_id: int):
            # many to many
            sql = select(self.model).options(joinedload(self.model.person)).where(self.model.id == data_id)
            # 第一种方式
            # queryset = await self.db.execute(sql)
            # datas = queryset.scalars().unique().all()
            # 第二种方式
            queryset = await self.db.scalars(sql)
            datas = queryset.unique().all()
            dataDict = {}
            for job in datas:
                dataDict.update(jsonable_encoder(job))
                dataDict["person"] = jsonable_encoder(job.person)

            return dataDict



