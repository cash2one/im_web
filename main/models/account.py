# -*- coding: utf-8 -*-
"""
"""
from config import MYSQL_GC
from ..god import God, A
from ..core import ObjectType, MainException, EmailUsageType, GrantType
from flask import current_app, url_for
from utils.func import random_ascii_string
from werkzeug.security import generate_password_hash, check_password_hash
from operator import or_
import time
import logging
from itsdangerous import URLSafeTimedSerializer
from config import SECRET_KEY, TOKEN_SALT

TOKEN_SALT_TYPE = 'oauth2'


def token_serializer(token_type):
    return URLSafeTimedSerializer(SECRET_KEY, salt="{}.{}".format(TOKEN_SALT, token_type))


def set_password(key, account_obj, pwd):
    if len(str(pwd)) >= 6:
        account_obj[key] = generate_password_hash(pwd)
        return

    raise MainException.ACCOUNT_PASSWORD_INVALID


def mask_to_permissions(mask):
    perms = []
    for i in xrange(0, 16):
        perm = (mask % 2) * (2 ** i)
        mask /= 2
        if perm:
            perms.append(perm)

    return perms


def permissions_to_mask(perms):
    if perms is None:
        return None

    # perms如果为()或者[]清空权限
    if perms:
        # 设置权限
        perms_val = reduce(or_, perms)
    else:
        # 清除权限
        perms_val = 0

    return perms_val


class Account(God):
    _db = MYSQL_GC
    _type = ObjectType.ACCOUNT
    _name = 'account'
    _table = 'account'

    _fields = (
        'id',
        'name',
        'email',
        A('email_removed', hidden=True),
        'email_checked',
        A('password', hidden=True, setter=set_password),
        'ctime',
        'role',
        'mobile_zone',
        'mobile'
    )

    def verify_email(self, email_cb):
        if email_cb is None:
            return
        mail = current_app.extensions.get('mail')
        code = random_ascii_string(40)
        if email_cb == 'debug':
            url = url_for('.confirm_email', code=code, _external=True)
        else:
            url = email_cb + code

        try:
            mail.send_message("新游开发者平台邮箱验证",
                              recipients=[self.email],
                              html="感谢注册新游开发者平台，使用新游开发者服务。<br/>"
                                   "请点击以下按钮进行邮箱验证，以便您正常使用新游开发者平台的更多功能：<br/>"
                                   "<a href=\"{url}\">马上验证邮箱</a> <br/>"
                                   "如果您无法点击以上链接，请复制以下网址到浏览器里直接打开：<br/>"
                                   "{url} <br/>"
                                   "如果您并未申请新游开发者平台的相关服务，可能是其他用户误输入了您的邮箱地址。请忽略此邮件。".format(url=url))
        except Exception, e:
            logging.exception(e)

        self.mysql.execute(
            "INSERT INTO verify_email (email, usage_type, code, ctime, ro_id) VALUES (%s,%s,%s,%s,%s)",
            (self.email, EmailUsageType.DEVELOPER_VERIFY, code, int(time.time()), self.id)
        )

    def forget_password(self, email_cb):
        if email_cb is None:
            return
        mail = current_app.extensions.get('mail')
        code = random_ascii_string(40)
        if email_cb == 'debug':
            url = url_for('.reset_password', code=code, _external=True)
        else:
            url = email_cb + code
        try:
            mail.send_message("新游开发者平台密码重置",
                              recipients=[self.email],
                              html="本邮件是应您在新游开发者平台上提交的重置密码请求，从而发到您邮箱的重置密码的邮件。<br/>"
                                   "如果您没有提交重置密码请求而收到此邮件，我们非常抱歉打扰您，请忽略本邮件。<br/>"
                                   "要重置您在新游开发者平台上的用户密码，请点击以下链接：<br/>"
                                   "<a href=\"{url}\">密码重置</a> <br/>"
                                   "该链接会在浏览器上打开一个页面，让您来重设密码。如果无法点击请复制到浏览器地址栏里：<br/>"
                                   "{url} <br/>"
                                   "上述地址24小时内有效。".format(url=url))
        except Exception, e:
            logging.exception(e)

        today_time = int(time.time())
        result = self.mysql.execute(
            "SELECT COUNT(0) AS email_count FROM verify_email "
            "WHERE email=%s AND usage_type=%s AND (ctime BETWEEN %s AND %s)",
            (self.email, EmailUsageType.DEVELOPER_RESET_PWD, today_time - 86400, today_time)
        )
        row = result.fetchone()
        if row['email_count'] > 5:
            raise MainException.EMAIL_TOO_OFTEN

        self.mysql.execute(
            "INSERT INTO verify_email (email, usage_type, code, ctime, ro_id) VALUES (%s,%s,%s,%s,%s)",
            (self.email, EmailUsageType.DEVELOPER_RESET_PWD, code, today_time, self.id)
        )

    def confirm_email(self, code, usage_type, expires_in=86400):
        result = self.mysql.execute("SELECT * FROM verify_email WHERE code=%s AND usage_type=%s",
                                    (code, usage_type))
        row = result.fetchone()
        done = None
        if row:
            if row['ctime'] + expires_in > time.time():
                done = row

            self.mysql.execute("DELETE FROM verify_email WHERE code=%s AND usage_type=%s",
                               (code, usage_type))

        return done

    def check_password(self, password):
        if password:
            return check_password_hash(self.password, password)

        return False

    def _gen_token(self, grant_type, client_id, ro_id, client_obj=None):
        token_length = 40

        time_now = int(time.time())

        token_type = 'Bearer'
        # 永不过期
        expires_in = 0
        refresh_token = random_ascii_string(token_length)
        access_token = token_serializer(TOKEN_SALT_TYPE).dumps((grant_type, client_id, ro_id, time_now, expires_in))

        # 保存token信息

        # 同一秒多次请求导致写入失败，使用REPLACE代替INSERT
        result = self.mysql.execute(
            "REPLACE INTO token (grant_type,access_token,expires_in,refresh_token,client_id,ro_id,ctime) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (grant_type, access_token, expires_in, refresh_token, client_id, ro_id, time_now)
        )

        if result:
            data = {
                'access_token': access_token,
                'token_type': token_type,
                'expires_in': expires_in,
                'refresh_token': refresh_token,
            }

            if client_obj:
                data['app_id'] = client_obj.app.id

            return data
        else:
            return None

    def get_token(self):
        return self._gen_token(GrantType.ACCOUNT_CREDENTIALS, 0, self.id)

