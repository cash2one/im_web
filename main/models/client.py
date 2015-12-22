# -*- coding: utf-8 -*-
"""
"""
from config import MYSQL_GC
from ..god import God
from ..core import ObjectType, PlatformType
import config
import redis
from utils.certificate import Certificate
import time


class Client(God):
    __slots__ = ('app',)
    _db = MYSQL_GC
    _type = ObjectType.CLIENT
    _name = 'client'
    _table = 'client'

    _fields = (
        'id',
        'app_id',
        'developer_id',
        'platform_type',
        'platform_identity',
        'ctime',
        'utime',
        'is_active'
    )

    def present(self):
        data = super(Client, self).present()
        for field, v in data.items():
            if field == 'developer_id':
                data['developer'] = {'id': v}
                del data['developer_id']

        if data['platform_type'] == PlatformType.IOS:
            apns = self.fetch_apns()
            data['apns'] = {
                'sandbox_key_secret': apns.get('sandbox_key_secret', ''),
                'sandbox_key_utime': apns.get('sandbox_key_utime', 0),
                'production_key_secret': apns.get('production_key_secret', ''),
                'production_key_utime': apns.get('production_key_utime', 0),
            }
        elif data['platform_type'] == PlatformType.ANDROID:
            data['certificate'] = self.get_certificate_url()

        return data

    def set_apns(self, sandbox_key, sandbox_key_secret, production_key, production_key_secret):
        import time

        row = self.fetch_apns()

        sandbox = {}
        if sandbox_key is None:
            if row.get('sandbox_key_utime'):
                sandbox['sandbox_key_utime'] = row.get('sandbox_key_utime')
        else:
            sandbox['sandbox_key'] = sandbox_key
            sandbox['sandbox_key_utime'] = int(time.time())

        if sandbox:
            if sandbox_key_secret:
                sandbox['sandbox_key_secret'] = sandbox_key_secret
                sandbox['sandbox_key_utime'] = int(time.time())

        production = {}
        if production_key is None:
            if row.get('production_key_utime'):
                production['production_key_utime'] = row.get('production_key_utime')
        else:
            production['production_key'] = production_key
            production['production_key_utime'] = int(time.time())

        if production:
            if production_key_secret:
                production['production_key_secret'] = production_key_secret
                production['production_key_utime'] = int(time.time())

        if row:
            params = []
            values = []

            if sandbox:
                params.extend(["{}=%s".format(field) for field in sandbox.keys()])
                values.extend(sandbox.values())

            if production:
                params.extend(["{}=%s".format(field) for field in production.keys()])
                values.extend(production.values())

            if params:
                sql = "UPDATE client_apns SET {} WHERE client_id=%s".format(','.join(params))
                values.append(self.get_id())
            else:
                sql = None
        else:
            data = {}

            if sandbox:
                data.update(sandbox)

            if production:
                data.update(production)

            if data:
                data['client_id'] = self.get_id()
                params = ['%s'] * len(data)
                sql = "INSERT INTO client_apns ({}) VALUES ({})".format(','.join(data.keys()), ','.join(params))
                values = data.values()
            else:
                sql = None

        if sql:
            if self.mysql.execute(sql, values):
                chan_rds = redis.StrictRedis(host=config.REDIS_DATA_HOST,
                                             port=config.REDIS_DATA_PORT,
                                             db=config.REDIS_DATA_DB,
                                             password=config.REDIS_DATA_PASSWORD)
                chan_rds.publish("apns_update_p12_channel", self.app_id)

                return {
                    'client_id': self.get_id(),
                    'sandbox_key_secret': sandbox.get('sandbox_key_secret', ''),
                    'sandbox_key_utime': sandbox.get('sandbox_key_utime', 0),
                    'production_key_secret': production.get('production_key_secret', ''),
                    'production_key_utime': production.get('production_key_utime', 0),
                }

        return None

    def fetch_apns(self):
        rs = self.mysql.execute(
                "SELECT sandbox_key_utime,sandbox_key_secret,production_key_utime,production_key_secret "
                "FROM client_apns WHERE client_id=%s",
                self.get_id()
        )

        return rs.fetchone() or {}

    def set_certificate(self, pkey=None, cer=None, xinge_access_id=None, xinge_secret_key=None, xiaomi_app_id=None,
                        xiaomi_secret_key=None):
        row = self.fetch_certificate()

        certificate = {}
        if pkey is not None and cer is not None:
            certificate['pkey'] = pkey
            certificate['cer'] = cer
            certificate['update_time'] = int(time.time())
        else:
            if row.get('update_time'):
                certificate['update_time'] = row.get('update_time')

        if xinge_access_id is not None and xinge_secret_key is not None:
            certificate['xinge_access_id'] = xinge_access_id
            certificate['xinge_secret_key'] = xinge_secret_key
            certificate['update_time'] = int(time.time())

        if xiaomi_app_id is not None and xiaomi_secret_key is not None:
            certificate['xiaomi_app_id'] = xiaomi_app_id
            certificate['xiaomi_secret_key'] = xiaomi_secret_key
            certificate['update_time'] = int(time.time())

        if row:
            params = []
            values = []

            if certificate:
                params.extend(["{}=%s".format(field) for field in certificate.keys()])
                values.extend(certificate.values())

            if params:
                sql = "UPDATE client_certificate SET {} WHERE client_id=%s".format(','.join(params))
                values.append(self.get_id())
            else:
                sql = None
        else:
            data = {}

            if certificate:
                data.update(certificate)

            if data:
                data['client_id'] = self.get_id()
                params = ['%s'] * len(data)
                sql = "INSERT INTO client_certificate ({}) VALUES ({})".format(','.join(data.keys()), ','.join(params))
                values = data.values()
            else:
                sql = None

        if sql:
            if self.mysql.execute(sql, values):
                return {
                    'client_id': self.get_id(),
                    'pkey': certificate.get('pkey', ''),
                    'cer': certificate.get('cer', ''),
                    'xinge_access_id': certificate.get('xinge_access_id', ''),
                    'xinge_secret_key': certificate.get('xinge_secret_key', ''),
                    'xiaomi_app_id': certificate.get('xiaomi_app_id', ''),
                    'xiaomi_secret_key': certificate.get('xiaomi_secret_key', ''),
                    'update_time': certificate.get('update_time', 0),
                }

        return None

    def fetch_certificate(self):
        rs = self.mysql.execute(
                "SELECT pkey, cer, xinge_access_id, xinge_secret_key, xiaomi_app_id, xiaomi_secret_key, update_time "
                "FROM client_certificate WHERE client_id=%s",
                self.get_id()
        )

        return rs.fetchone() or {}

    def get_certificate_url(self):
        certificate = self.fetch_certificate()
        return {
            'pkey_url': Certificate.create_download_url(self.get_id(), 'pkey', self.ctime),
            'cer_url': Certificate.create_download_url(self.get_id(), 'cer', self.ctime),
            'xinge_access_id': certificate.get('xinge_access_id'),
            'xinge_secret_key': certificate.get('xinge_secret_key'),
            'xiaomi_app_id': certificate.get('xiaomi_app_id'),
            'xiaomi_secret_key': certificate.get('xiaomi_secret_key')
        }
