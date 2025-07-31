#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/8/8 11:02
# @File           : auth_util.py
# @IDE            : PyCharm
# @desc           : 简要说明

from datetime import datetime, timedelta
from fastapi import Request
from application import settings
import jwt
from apps.vadmin.auth import models
from core.database import redis_getter
from utils.sms.code import CodeSMS
from .validation import LoginValidation, LoginForm, LoginResult, OTP


class LoginManage:
    """
    登录认证工具
    """

    @LoginValidation
    async def password_login(self, data: LoginForm, user: models.VadminUser, **kwargs) -> LoginResult:
        """
        验证用户密码
        """
        result = models.VadminUser.verify_password(data.password, user.password)

        if not result:
            return LoginResult(status=False, msg="密码错误")

        # secret为空的时候
        if not user.secret and user.is_reset_password == 0:
            if data.otp == '000000':
                return LoginResult(status=True, msg="验证成功")
            else:
                return LoginResult(status=False, msg="验证码错误")

        resOtp = OTP.verify_otp(user.secret, data.otp)
        if not resOtp:
            return LoginResult(status=False, msg="验证码错误")

        if result and resOtp:
            return LoginResult(status=True, msg="验证成功")
        return LoginResult(status=False, msg="手机号 或 密码错误 或 验证码错误")

    @LoginValidation
    async def sms_login(self, data: LoginForm, request: Request, **kwargs) -> LoginResult:
        """
        验证用户短信验证码
        """
        rd = redis_getter(request)
        sms = CodeSMS(data.telephone, rd)
        result = await sms.check_sms_code(data.password)
        if result:
            return LoginResult(status=True, msg="验证成功")
        return LoginResult(status=False, msg="验证码错误")

    @staticmethod
    def create_token(payload: dict, expires: timedelta = None):
        """
        创建一个生成新的访问令牌的工具函数。

        pyjwt：https://github.com/jpadilla/pyjwt/blob/master/docs/usage.rst
        jwt 博客：https://geek-docs.com/python/python-tutorial/j_python-jwt.html

        #TODO 传入的时间为UTC时间datetime.datetime类型，但是在解码时获取到的是本机时间的时间戳
        """
        if expires:
            expire = datetime.utcnow() + expires
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload.update({"exp": expire})
        encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
