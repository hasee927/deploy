#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/03/05
# @IDE            : PyCharm
# @desc           : 查询参数-类依赖项

"""
类依赖项-官方文档：https://fastapi.tiangolo.com/zh/tutorial/dependencies/classes-as-dependencies/
"""
from fastapi import Depends, Query
from core.dependencies import Paging, QueryParams



class BankWaterParams(QueryParams):
    """
    列表分页
    """

    def __init__(
            self,
            name: str | None = Query(None, title="短信ID"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.name = ("like", name)


