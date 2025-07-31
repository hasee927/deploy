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

class FundWaterParams(QueryParams):
    """
    列表分页
    """
    def __init__(
            self,
            merchant_id: str | None = Query(None, title="商户ID"),
            water_type: str | None = Query(None, title="流水类型"),
            bill_no: str | None = Query(None, title="所属单号"),
            from_date: str | None = Query(None, title="开始时间"),
            to_date: str | None = Query(None, title="结束时间"),
            sign: str | None = Query(None, title="sign"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.merchant_id = merchant_id
        self.water_type = water_type
        self.bill_no = bill_no
        self.from_date = from_date
        self.to_date = to_date
        self.sign = sign



class SignFundWaterParams(QueryParams):
    """
    列表分页
    """
    def __init__(
            self,
            merchant_id: str = Query(None, title="商户ID"),
            sign: str = Query(None, title="sign"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.merchant_id = merchant_id
        self.sign = sign
