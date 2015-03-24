# -*- coding: utf-8 -*-
from utils.mysql import get_mysql
from config import MYSQL
from collections import OrderedDict

class Developer(object):
    @classmethod
    def get_app_ids(cls, developer_id, offset=0, limit=20):
        """
        :param offset:
        :param limit:
        :return:
        [
            {
                "id": "",
                "platform_type": "",
                "app_id": "",
                "app_name": ""
            },
            ...
        ]
        """
        mysql = get_mysql(MYSQL)

        rs = mysql.execute(
            "SELECT app.id, app.name, client.platform_type "
            "FROM app JOIN client ON app.id = client.app_id "
            "WHERE client.developer_id=%s AND client.is_active=1",
            (developer_id, )
        )

        data = OrderedDict()
        for row in rs.fetchall():
            if row['id'] not in data:
                data[row['id']] = {
                    'id': row['id'],
                    'name': row['name'],
                    'platform_types': [row['platform_type']],
                }
            else:
                data[row['id']]['platform_types'].append(row['platform_type'])

        result = data.values()

        return result[offset:offset+limit], len(result)