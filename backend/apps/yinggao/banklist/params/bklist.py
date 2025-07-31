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



class BankListParams(QueryParams):
    """
    列表分页
    """

    def __init__(
            self,
            params: Paging = Depends(),
            bank_name: str | None = Query(None, title="银行名称"),
            channel_code: str | None = Query(None, title="通道code"),
            bank_utr: str | None = Query(None, title="银行UTR"),
            info_sources: str | None = Query(None, title="信息来源"),
            match_type: str | None = Query(None, title="匹配类型"),
            collection_type: str | None = Query(None, title="收款类型"),

    ):
        super().__init__(params)
        self.bank_name = ("like", bank_name)
        self.channel_code = ("like", channel_code)
        self.bank_utr = ("like", bank_utr)
        self.info_sources = ("like", info_sources)
        self.match_type = ("like", match_type)
        self.collection_type = ("like", collection_type)
        self.v_order = "desc"
        self.v_order_field = "id"
