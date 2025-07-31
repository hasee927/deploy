#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/18 22:19
# @File           : role.py
# @IDE            : PyCharm
# @desc           : 查询参数-类依赖项

"""
类依赖项-官方文档：https://fastapi.tiangolo.com/zh/tutorial/dependencies/classes-as-dependencies/
"""
from fastapi import Depends, Query
from core.dependencies import Paging, QueryParams



class ChannelParams(QueryParams):
    """
    列表分页
    """

    def __init__(
            self,
            channel_code: str | None = Query(None, title="通道code"),
            channel_type: str | None = Query(None, title="通道类型"),
            channel_status: str | None = Query(None, title="通道状态"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.channel_code = ("like", channel_code)
        self.channel_type = ("like", channel_type)
        self.channel_status = ("like", channel_status)
        self.v_order = "desc"
        self.v_order_field = "id"

