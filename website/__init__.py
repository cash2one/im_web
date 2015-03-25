# -*- coding: utf-8 -*-
""" 接口加载器
包含相对路径import的python脚本不能直接运行，只能作为module被引用。
"""
from flask import g, request, render_template
from utils.pager import Pager
from utils.response_meta import ResponseMeta
from utils.request import Request
from utils.func import init_logger

LOGGER = init_logger(__name__)


def http_error_handler(err):
    LOGGER.error(err)
    return render_template('error.html', description=str(err))


def response_meta_handler(response_meta):
    return response_meta.get_response()


def before_request():
    g.headers = {}
    g.pagination = Pager(request.args)
    g.request = Request(request)
    g.auth = None
    g.perms = {}


def app_teardown(exception):
    # LOGGER.debug('app_teardown')
    mysql_instances = getattr(g, '_mysql_instances', None)
    if mysql_instances is not None:
        for mysql in mysql_instances.values():
            mysql.close()


# 初始化接口
def init_app(app):
    app.teardown_appcontext(app_teardown)
    app.before_request(before_request)
    for error in range(400, 420) + range(500, 506):
        app.error_handler_spec[None][error] = http_error_handler
    app.register_error_handler(ResponseMeta, response_meta_handler)

    from utils.mail import Mail
    from utils.sentry import Sentry

    Mail.init_app(app)
    Sentry.init_app(app)
    # 注册接口
    from api import api
    from web import web

    app.register_blueprint(web)
    app.register_blueprint(api)