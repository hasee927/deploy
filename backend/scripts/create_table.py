# -*- coding: utf-8 -*-
# import pymysql
# pymysql.install_as_MySQLdb()

from db.db_base import BaseModel
from sqlalchemy import create_engine
from application.settings import CREATE_TABLE_DATABASE_URL
from apps.bank.iob import models as bank_iob_models
from apps.bank.bank import models as bank_bank_models
from apps.company import models as company_models

###########################业务应用#################################
from apps.yinggao.channellist import models as channel_models
from apps.yinggao.bankconfig import models as bank_models
from apps.yinggao.collectionorder.models.collorder import Collect_Order
from apps.yinggao.proxypayorder import models as proxypayorder_models
from apps.yinggao.banklist import models as bklist_models
# from apps.yinggao.merchantlist import models as merchantlist_models
from apps.yinggao.smsconfig import models as smsconfig_models
from apps.yinggao.botconfig import models as botconfig_models
from apps.yinggao.orderstat import models as order_models
from apps.yinggao.finance import models as finance_models
from apps.yinggao.fundwater import models as fundwater_models
from apps.yinggao.paymentdetail import models as paymentdetail_models
from apps.yinggao.uploadbankwater import models as bankwater_models
from apps.yinggao.botgroup import models as group_models


class CreateTables:
    """
    创建表
    """
    engine = create_engine(CREATE_TABLE_DATABASE_URL, echo=True)
    def __init__(self):
        self.create_table = None
        self.base = BaseModel

    def run(self):
        """
        开始创建表
        """
        # 创建表实例
        # self.create_table = bank_iob_models.Bank_Iob
        # self.create_table = bank_bank_models.Bank

        # self.create_table = company_models.Department
        # self.create_table = company_models.Employee

        # self.create_table = company_models.companyPerson
        # self.create_table = company_models.companyJob
        # self.create_table = company_models.company_person_job


        ###########################业务应用###################################

        # 银行配置
        # self.create_table = bank_models.BankConfigure
        # 代收订单
        # self.create_table = Collect_Order


        # 代付订单
        # self.create_table = proxypayorder_models.Proxy_Pay_Order
        # 银行列表
        # self.create_table = bklist_models.Banklist
        # 通道列表
        # self.create_table = channel_models.ChannelDataList
        # 商户列表
        # self.create_table = merchantlist_models.MerchantList

        # 短信列表
        # self.create_table = smsconfig_models.SmsList

        # 短信列表
        # self.create_table = botconfig_models.BotConfig

        # 成功订单
        # self.create_table = order_models.Order_Success

        # 商户资金
        # self.create_table = finance_models.Finance

        # 资金流水
        # self.create_table = fundwater_models.FundWater


        # 打款明细
        # self.create_table = paymentdetail_models.PaymentDetail

        # 上传银行流水按钮列表
        # self.create_table = bankwater_models.BankWater


        # 机器人群列表
        # self.create_table = group_models.BotGroup

        # ########################################################################
        # 执行创建
        # self.base.metadata.create_all(bind=self.engine)


if __name__ == "__main__":
    ct = CreateTables()
    ct.run()
