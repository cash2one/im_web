# -*- coding: utf-8 -*-
"""
"""
from config import MYSQL_GC
from ..god import God
from ..core import ObjectType, PlatformType, MainException

class App(God):
    _db = MYSQL_GC
    _type = ObjectType.APP
    _name = 'app'
    _table = 'app'

    _fields = (
        'id',
        'name',  # 名称
        'developer_id',  # 开发者ID
        'ctime',  # 创建时间
        'key',  # app key
        'secret',  # app secret
        'status'  # 应用状态
    )

    _collections = ('clients', )

    def delete_by_developer(self, developer_id):
        rs = self.mysql.execute("SELECT id FROM client WHERE app_id=%s AND developer_id=%s",
                                (self.get_id(), developer_id))
        client_ids = [str(row['id']) for row in rs.fetchall()]
        if client_ids:
            self.mysql.execute("DELETE FROM client WHERE id IN ({})".format(','.join(client_ids)))

        self.mysql.execute("DELETE FROM app WHERE id=%s AND developer_id=%s", (self.get_id(), developer_id))

    def put_clients(self, input_clients):
        client_kvs = {}
        for platform_type in PlatformType.get_dict().values():
            client_obj = Client()
            client_obj.platform_type = platform_type
            client_obj.app_id = self.get_id()

            clients = client_obj.find()
            if clients:
                client_obj = clients[0]
            else:
                client_obj.init()
                client_obj.is_active = 0
                client_obj.developer_id = self.developer_id

            client_kvs[platform_type] = client_obj

        for row in input_clients:
            platform_type = int(row['platform_type'])
            client_obj = client_kvs.get(platform_type)
            if not client_obj:
                raise MainException.CLIENT_INVALID_PLATFORM_TYPE

            client_obj.platform_identity = row.get('platform_identity')
            client_obj.is_active = row.get('is_active')

        clients = client_kvs.values()

        active_count = 0
        for client_obj in clients:
            active_count += client_obj.is_active

        result = []
        if not active_count:
            raise MainException.APP_NO_ACTIVE_CLIENT
        else:
            for client_obj in clients:
                if client_obj._add_delay:
                    client_obj.add()
                else:
                    client_obj.save()

                c = {'platform_type': client_obj.platform_type,
                     'platform_identity': client_obj.platform_identity,
                     'is_active': client_obj.is_active,
                     'id': client_obj.get_id()
                     }
                if client_obj.platform_type == PlatformType.ANDROID:
                    c['certificate'] = client_obj.get_certificate_url()
                result.append(c)

        self.clients = result

    def set_clients(self, val):
        return val

    def get_clients(self):
        client_kvs = {}

        client_obj = Client()
        client_obj.app_id = self.get_id()
        client_arr = client_obj.find()
        if client_arr:
            for client in client_arr:
                client_kvs[client['platform_type']] = {'platform_type': client.platform_type,
                                                       'platform_identity': client.platform_identity,
                                                       'is_active': client.is_active,
                                                       'id': client.get_id()
                                                       }

                if client.platform_type == PlatformType.IOS:
                    apns = client.fetch_apns()
                    client_kvs[client['platform_type']]['apns'] = {
                        'sandbox_key_secret': apns.get('sandbox_key_secret', ''),
                        'sandbox_key_utime': apns.get('sandbox_key_utime', 0),
                        'production_key_secret': apns.get('production_key_secret', ''),
                        'production_key_utime': apns.get('production_key_utime', 0),
                    }
                elif client.platform_type == PlatformType.ANDROID:
                    client_kvs[client['platform_type']]['certificate'] = client.get_certificate_url()

        return client_kvs.values()

    def validate(self):
        if not self.name or not self.developer_id:
            raise MainException.APP_LACK_PARAMS

    def present(self):
        data = super(App, self).present()

        for field, v in data.items():
            if field == 'developer_id':
                data['developer'] = {'id': v}
                del data[field]

        return data


from .client import Client