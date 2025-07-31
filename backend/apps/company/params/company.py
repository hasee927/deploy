from fastapi import Depends, Query
from core.dependencies import Paging, QueryParams



class DeptParams(QueryParams):
    """
    列表分页
    """
    def __init__(
            self,
            name: str | None = Query(None, title="部门名称"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.name = ("like", name)


class EmpParams(QueryParams):
    """
    列表分页
    """
    def __init__(
            self,
            name: str | None = Query(None, title="员工名称"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.name = ("like", name)



class PersonParams(QueryParams):
    """
    列表分页
    """
    def __init__(
            self,
            name: str | None = Query(None, title="个人名称"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.name = ("like", name)


class JobParams(QueryParams):
    """
    列表分页
    """
    def __init__(
            self,
            name: str | None = Query(None, title="工作名称"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.name = ("like", name)