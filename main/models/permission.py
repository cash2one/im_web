# -*- coding: utf-8 -*-
""" OAuth 2.0 Resource
"""
from flask import request, g
from werkzeug.wrappers import Response
import time
from functools import wraps
from utils.util import make_response
from itsdangerous import URLSafeTimedSerializer

from config import SECRET_KEY, TOKEN_SALT, MYSQL
from utils.mysql import get_mysql

TOKEN_SALT_TYPE = 'oauth2'


def INVALID_ACCESS_TOKEN():
    return make_response(400, code=1003, msg="client无权限")


class GrantType(object):
    SMS_CODE = 1
    CLIENT_CREDENTIALS = 2
    ACCOUNT_CREDENTIALS = 3
    SNS_TOKEN = 4


class RoleType(object):
    """角色对象类型
    """
    DEVELOPER = 1
    CHANNEL = 2
    PLATFORM = 3


def token_serializer(token_type):
    return URLSafeTimedSerializer(SECRET_KEY, salt="{}.{}".format(TOKEN_SALT, token_type))


def mask_to_permissions(mask):
    perms = []
    for i in xrange(0, 16):
        perm = (mask % 2) * (2 ** i)
        mask /= 2
        if perm:
            perms.append(perm)

    return perms


class ResourceAuthorization(object):
    # 授权错误
    error = None
    # 是否正确
    is_valid = False
    # 第三方客户端id
    client_id = None
    # 资源所有者id
    ro_id = None
    # 授权类型
    grant_type = None

    def is_invalid(self):
        if self.error is not None or not self.is_valid:
            return True

        return False


class OAuth2Resource(object):
    def __init__(self):
        self.token_serializer = token_serializer(TOKEN_SALT_TYPE)

    def get_authorization(self):
        auth = ResourceAuthorization()
        header = self.get_authorization_header()
        if not header or not header.split:
            auth.error = Response(status=401)
            return auth

        header = header.split()
        if len(header) > 1 and header[0] == 'Bearer':
            access_token = header[1]
            self.validate_access_token(access_token, auth)
            if not auth.is_valid:
                auth.error = Response(status=401)

        return auth

    @staticmethod
    def get_authorization_header():
        if 'Authorization' in request.headers:
            return request.headers['Authorization']
        else:
            return None

    def validate_access_token(self, access_token, auth):
        try:
            row = self.token_serializer.loads(access_token)
        except:
            return

        if row:
            grant_type, client_id, ro_id, ctime, expires_in = row

            auth.grant_type = grant_type
            # 过期时间为0为不过期
            if expires_in == 0 or (ctime + expires_in) > time.time():
                auth.is_valid = True
                auth.client_id = client_id
                auth.ro_id = ro_id
