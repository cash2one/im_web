# -*- coding: utf-8 -*-
from utils.mysql import get_mysql
from config import MYSQL


class Developer(object):
    @classmethod
    def get_app_ids(cls, id, app_type=1, offset=0, limit=20):
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
            "SELECT SQL_CALC_FOUND_ROWS client.id,client.secret, client.platform_type,client.app_id,app.name,app.app_type FROM client "
            "LEFT JOIN app ON (client.app_id=app.id) "
            "WHERE client.developer_id=%s AND client.is_active=1 AND app.app_type = %s LIMIT %s,%s",
            (id, app_type, offset, limit)
        )

        data = []
        for row in rs.fetchall():
            data.append({
                'id': row['id'],
                'platform_type': row['platform_type'],
                'secret': row['secret'],
                'app_id': row['app_id'],
                'app_name': row['name'],
                'app_type': row['app_type']
            })

        return data, mysql.rows_found()