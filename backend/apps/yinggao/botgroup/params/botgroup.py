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



class BotParams(QueryParams):
    """
    列表分页
    """

    def __init__(
            self,
            chat_id: str | None = Query(None, title="群聊ID"),
            name: str | None = Query(None, title="群名称"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.chat_id = ("like", chat_id)
        self.name = ("like", name)

