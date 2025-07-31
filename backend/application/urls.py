# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/19 15:47
# @File           : urls.py
# @IDE            : PyCharm
# @desc           : 路由文件

from apps.vadmin.auth.utils.login import app as auth_app
from apps.vadmin.auth.views import app as vadmin_auth_app
from apps.vadmin.system.views import app as vadmin_system_app
from apps.vadmin.record.views import app as vadmin_record_app
from apps.vadmin.workplace.views import app as vadmin_workplace_app
from apps.vadmin.analysis.views import app as vadmin_analysis_app
from apps.vadmin.help.views import app as vadmin_help_app
from apps.vadmin.resource.views import app as vadmin_resource_app
# 测试接口
from apps.bank.bank.views import app as bank_app
from apps.bank.iob.views import app as iob_getData_app
# 测试外键
from apps.company.views import app as company_app

###################################业务应用####################################
from apps.yinggao.channellist.views import app as channellist_app
from apps.yinggao.bankconfig.views import app as bankcfg_app
from apps.yinggao.collectionorder.views import app as collectionorder_app
from apps.yinggao.proxypayorder.views import app as proxypayorder_app
from apps.yinggao.banklist.views import app as bklist_app
from apps.yinggao.merchantlist.views import app as merchant_app
from apps.yinggao.smsconfig.views import app as sms_app
from apps.yinggao.botconfig.views import app as bot_app
from apps.yinggao.orderstat.views import app as order_app
from apps.yinggao.finance.views import app as finance_app
from apps.yinggao.fundwater.views import app as fundwater_app
from apps.yinggao.paymentdetail.views import app as paydetail_app
from apps.yinggao.uploadbankwater.views import app as bankwater_app
from apps.yinggao.botgroup.views import app as group_app


# 引入应用中的路由
urlpatterns = [
    {"ApiRouter": auth_app, "prefix": "/auth", "tags": ["系统认证"]},
    {"ApiRouter": vadmin_auth_app, "prefix": "/vadmin/auth", "tags": ["权限管理"]},
    {"ApiRouter": vadmin_system_app, "prefix": "/vadmin/system", "tags": ["系统管理"]},
    {"ApiRouter": vadmin_record_app, "prefix": "/vadmin/record", "tags": ["记录管理"]},
    {"ApiRouter": vadmin_workplace_app, "prefix": "/vadmin/workplace", "tags": ["工作区管理"]},
    {"ApiRouter": vadmin_analysis_app, "prefix": "/vadmin/analysis", "tags": ["数据分析管理"]},
    {"ApiRouter": vadmin_help_app, "prefix": "/vadmin/help", "tags": ["帮助中心管理"]},
    {"ApiRouter": vadmin_resource_app, "prefix": "/vadmin/resource", "tags": ["资源管理"]},
    # 测试接口
    {"ApiRouter": bank_app, "prefix": "/bank", "tags": ["银行接口"]},
    {"ApiRouter": iob_getData_app, "prefix": "/bank/iob", "tags": ["测试接口"]},
    # 测试外键
    {"ApiRouter": company_app, "prefix": "/company", "tags": ["测试外键"]},

    ###################################业务应用####################################
    {"ApiRouter": channellist_app, "prefix": "/yg/channel", "tags": ["通道列表"]},
    {"ApiRouter": bankcfg_app, "prefix": "/yg/bank", "tags": ["银行配置"]},
    {"ApiRouter": order_app, "prefix": "/yg/order", "tags": ["订单统计"]},
    {"ApiRouter": collectionorder_app, "prefix": "/yg/collorder", "tags": ["代收订单"]},
    {"ApiRouter": proxypayorder_app, "prefix": "/yg/pporder", "tags": ["代付订单"]},
    {"ApiRouter": bklist_app, "prefix": "/yg/bklist", "tags": ["银行列表"]},
    {"ApiRouter": merchant_app, "prefix": "/yg/merchant", "tags": ["商户列表"]},
    {"ApiRouter": sms_app, "prefix": "/yg/sms", "tags": ["短信列表"]},
    {"ApiRouter": bot_app, "prefix": "/yg/bot", "tags": ["机器人列表"]},
    {"ApiRouter": finance_app, "prefix": "/yg/finance", "tags": ["商户资金"]},
    {"ApiRouter": fundwater_app, "prefix": "/yg/fund", "tags": ["资金流水"]},
    {"ApiRouter": paydetail_app, "prefix": "/yg/paydetail", "tags": ["打款明细"]},
    {"ApiRouter": bankwater_app, "prefix": "/yg/btn", "tags": ["上传银行流水按钮列表"]},
    {"ApiRouter": group_app, "prefix": "/yg/group", "tags": ["群聊列表"]},

]
