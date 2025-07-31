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



class SmsParams(QueryParams):
    """
    列表分页
    """

    def __init__(
            self,
            sms_id: str | None = Query(None, title="短信ID"),
            channel_code: str | None = Query(None, title="通道名称"),
            sms_type: str | None = Query(None, title="短信类型"),
            context: str | None = Query(None, title="短信内容"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.sms_id = ("like", sms_id)
        self.channel_code = ("like", channel_code)
        self.sms_type = ("like", sms_type)
        self.context = ("like", context)
        self.v_order = "desc"
        self.v_order_field = "id"

