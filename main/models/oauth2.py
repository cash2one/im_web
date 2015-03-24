# -*- coding: utf-8 -*-
""" OAuth 2.0 Provider
"""
from flask import request
from utils.mysql import get_mysql
import time
from ..core import MainException, token_serializer
from config import MYSQL_GC

TOKEN_SALT_TYPE = 'oauth2'


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
        self.mysql = get_mysql(MYSQL_GC)
        self.token_serializer = token_serializer(TOKEN_SALT_TYPE)

    def get_authorization(self):
        auth = ResourceAuthorization()
        header = self.get_authorization_header()
        if not header or not header.split:
            auth.error = MainException.UNAUTHORIZED
            return auth

        header = header.split()
        if len(header) > 1 and header[0] == 'Bearer':
            access_token = header[1]
            self.validate_access_token(access_token, auth)
            if not auth.is_valid:
                auth.error = MainException.UNAUTHORIZED

        return auth

    @staticmethod
    def get_authorization_header():
        if 'HTTP_AUTHORIZATION' in request.environ:
            return request.environ.get('HTTP_AUTHORIZATION')
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

