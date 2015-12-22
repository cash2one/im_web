# -*- coding: utf-8 -*-
from flask import session, request, g, render_template, url_for, abort, Response, redirect

from website.web import web
from website.blueprint_utils import login_required

from config import CA_CER, CA_KEY
from main.models.platform import Developer
from main.models.app import App, Client
from main.core import PlatformType
from utils.certificate import Certificate
from utils.crypt import Md5Utils
from utils.func import random_ascii_string
from main.god import And, Exp
import os
import time


def _im_login_required(f):
    return login_required(f, redirect_url_for='.im_index')


@web.route('/im')
@_im_login_required
def im_index():
    """
    IM 模块首页

    """

    g.uri_path = request.path
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 10))

    data, rows_found = Developer.get_app_ids(session['user']['id'], offset=offset, limit=limit)
    g.pagination.setdefault()
    g.pagination.rows_found = rows_found
    g.pagination.limit = limit
    g.pagination.offset = offset

    return render_template('im/index.html',
                           data={'offset': offset, 'list': data,
                                 'pagination': g.pagination,
                                 })


@web.route('/im/game/add')
@_im_login_required
def im_game_add():
    """
    创建游戏
    """
    data = {}
    data['method'] = 'add'
    data["game"] = {}
    data["game"]["name"] = ""
    data["game"]["id"] = ""
    data["game"]["major_category"] = {}
    data["game"]["minor_category"] = {}
    data["game"]["clients"] = [{'platform_type': PlatformType.ANDROID, 'is_active': 0},
                               {'platform_type': PlatformType.IOS, 'is_active': 0}]

    g.uri_path = request.path
    return render_template('im/game/add.html', data=data)


@web.route('/im/apps', methods=['POST'])
@_im_login_required
def im_apps_add():
    """
    创建游戏
    """
    g.uri_path = request.path

    app_obj = App()
    with app_obj.transaction():
        app_obj.init()
        if app_obj.feed(developer_id=session['user']['id'],
                        name=request.form.get('name'),
                        key=random_ascii_string(32),
                        secret=random_ascii_string(32),
                        status=int(request.form.get('status', 0))
                        ):

            clients = _get_clients()

            app_obj.put_clients(clients)

            ios_client_id = None
            android_client_id = None
            for clt in app_obj.clients():
                if int(clt['platform_type']) == PlatformType.IOS:
                    if clt['is_active']:
                        ios_client_id = clt['id']
                elif int(clt['platform_type']) == PlatformType.ANDROID:
                    # 不管是否激活都生成证书
                    android_client_id = clt['id']

            # 更新apns证书
            _update_apns(ios_client_id, clients, app_obj.id)

            if android_client_id is not None:
                crypto = Certificate(CA_KEY, CA_CER)
                pkey, cer = crypto.create_client_certificate(android_client_id)

                client_obj = Client().set_id(android_client_id)
                xinge_access_id = None
                xinge_secret_key = None
                if request.form.get('xinge_access_id') and request.form.get('xinge_secret_key'):
                    xinge_access_id = request.form.get('xinge_access_id')
                    xinge_secret_key = request.form.get('xinge_secret_key')

                xiaomi_app_id = None
                xiaomi_secret_key = None
                if request.form.get('xiaomi_app_id') and request.form.get('xiaomi_secret_key'):
                    xiaomi_app_id = request.form.get('xiaomi_app_id')
                    xiaomi_secret_key = request.form.get('xiaomi_secret_key')

                client_obj.set_certificate(pkey, cer, xinge_access_id, xinge_secret_key, xiaomi_app_id,
                                           xiaomi_secret_key)

            return redirect(url_for('.im_game_complete', game_id=app_obj.id))
    return redirect(url_for('.im_game_add'))


@web.route('/im/game/publish/<int:app_id>', methods=['GET'])
@_im_login_required
def im_apps_publish(app_id):
    """
    修改应用
    """
    app_obj = _get_app(app_id)
    app_obj.feed(developer_id=session['user']['id'],
                 status=1,
                 publish_time=int(time.time())
                 )
    return redirect(url_for('.im_game_detail', game_id=app_id, game=app_id, name=request.form.get('name')))


@web.route('/im/apps/<int:app_id>', methods=['POST'])
@_im_login_required
def im_apps_edit(app_id):
    """
    修改应用
    """
    g.uri_path = request.path

    app_obj = _get_app(app_id)
    app_obj.feed(developer_id=session['user']['id'],
                 name=request.form.get('name', app_obj['name']),
                 status=int(request.form.get('status', app_obj['status']))
                 )

    clients = _get_clients()

    app_obj.put_clients(clients)

    ios_client_id = None
    for clt in app_obj.clients():
        if int(clt['platform_type']) == PlatformType.IOS:
            if clt['is_active']:
                ios_client_id = clt['id']
        elif int(clt['platform_type']) == PlatformType.ANDROID:
            if clt['is_active']:
                if request.form.get('xinge_access_id') and request.form.get('xinge_secret_key'):
                    xinge_access_id = request.form.get('xinge_access_id')
                    xinge_secret_key = request.form.get('xinge_secret_key')

                    client_obj = Client().set_id(clt['id'])
                    client_obj.set_certificate(xinge_access_id=xinge_access_id, xinge_secret_key=xinge_secret_key)

                if request.form.get('xiaomi_app_id') and request.form.get('xiaomi_secret_key'):
                    xiaomi_app_id = request.form.get('xiaomi_app_id')
                    xiaomi_secret_key = request.form.get('xiaomi_secret_key')

                    client_obj = Client().set_id(clt['id'])
                    client_obj.set_certificate(xiaomi_app_id=xiaomi_app_id, xiaomi_secret_key=xiaomi_secret_key)

    # 更新apns证书
    _update_apns(ios_client_id, clients, app_id)

    return redirect(url_for('.im_game_detail', game_id=app_id, game=app_id, name=request.form.get('name')))


@web.route('/im/download/<string:path>', methods=['GET'])
def download(path):
    client_id, cer_type, request_time, sign = Certificate.get_download_data(path)
    client_obj = Client().set_id(int(client_id)).find()

    if not client_obj:
        abort(404)

    data = str(client_id) + "," + str(cer_type) + "," + str(request_time)

    if not Md5Utils.verify(data, sign, str(client_obj.ctime)):
        abort(403)

    cer = client_obj.fetch_certificate()
    if not cer:
        return ''

    f = cer.get(cer_type)
    if f:
        if cer_type == 'pkey':
            ext = 'key'
        else:
            ext = cer_type

        return Response(f,
                        mimetype="text/plain",
                        headers={"Content-Disposition": "attachment;filename=" + client_id + "." + ext})
    else:
        return ''


@web.route('/im/game/<int:game_id>')
@_im_login_required
def im_game_edit(game_id):
    """
    创建游戏
    """
    g.uri_path = request.path
    if game_id:
        game = _get_app(game_id).present()
        return render_template('im/game/edit.html', data={'game': game, 'method': 'edit'})


def push_common():
    g.uri_path = request.path
    game = request.args.get('game', '')
    name = request.args.get('name', '')
    return {'game': game, 'appname': name}


@web.route('/im/game/complete/<int:game_id>')
@_im_login_required
def im_game_complete(game_id):
    """
    游戏创建完成
    """
    data = push_common()
    g.uri_path = request.path
    offset = request.args.get('offset', 0)
    if game_id:
        data['game'] = _get_app(game_id).present()
        data['offset'] = offset
        # print data
        return render_template('im/game/complete.html', data=data)
    else:
        abort(404)


@web.route('/im/game/detail/<int:game_id>')
@_im_login_required
def im_game_detail(game_id):
    """
    游戏详情
    """
    data = push_common()
    g.uri_path = request.path
    offset = request.args.get('offset', 0)
    if game_id:
        data['gamedata'] = _get_app(game_id).present()
        data['offset'] = offset
        # print data
        return render_template('im/game/detail.html', data=data)
    else:
        abort(404)


def _get_app(app_id):
    app_arr = App().find_all(And(Exp('`developer_id`=%s', session['user']['id']),
                                 Exp('`id`=%s', app_id)))
    if not app_arr:
        abort(404)

    app_obj = app_arr[0]
    return app_obj


def _get_clients():
    clients = []

    if request.form.get('android_identity'):
        clients.append({
            'platform_type': PlatformType.ANDROID,
            'platform_identity': request.form.get('android_identity'),
            'is_active': 1,
        })

    if request.form.get('ios_identity'):
        clients.append({
            'platform_type': PlatformType.IOS,
            'platform_identity': request.form.get('ios_identity'),
            'is_active': 1,
        })
    return clients


def _update_apns(ios_client_id, clients, app_id):
    if ios_client_id is not None:
        for clt in clients:
            if int(clt['platform_type']) == PlatformType.IOS:
                sandbox_key_file = request.files.get('sandbox_key')
                if sandbox_key_file:
                    filename = sandbox_key_file.filename
                    ext = os.path.splitext(filename)[1]
                    if ext == '.p12':
                        sandbox_key = sandbox_key_file.read()
                        sandbox_key_secret = request.form.get('sandbox_key_secret')
                    else:
                        sandbox_key = None
                        sandbox_key_secret = None

                else:
                    sandbox_key = None
                    sandbox_key_secret = None

                production_key_file = request.files.get('production_key')
                if production_key_file:
                    filename = production_key_file.filename
                    ext = os.path.splitext(filename)[1]
                    if ext == '.p12':
                        production_key = production_key_file.read()
                        production_key_secret = request.form.get('production_key_secret')
                    else:
                        production_key = None
                        production_key_secret = None

                else:
                    production_key = None
                    production_key_secret = None

                client_obj = Client().set_id(ios_client_id)
                client_obj.feed(app_id=app_id)

                client_obj.set_apns(sandbox_key, sandbox_key_secret, production_key, production_key_secret)
