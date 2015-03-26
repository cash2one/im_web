# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, send_from_directory
import os
from utils.func import init_logger

LOGGER = init_logger(__name__)

web = Blueprint('web', __name__, template_folder='templates', static_folder='static')


@web.errorhandler
def generic_error_handler(err):
    LOGGER.exception(err)
    return render_template('error.html', description=str(err)), 500


@web.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(os.path.dirname(web.root_path), 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


import website.views


@web.route('/')
def index():
    return render_template('index/index.html')


@web.route('/contact')
def contact():
    return render_template('index/contact.html')

@web.route('/price')
def price():
    return render_template('index/price.html')

@web.route('/doc')
def doc():
    return '文档中心'


@web.route('/about')
def about():
    return '关于我们'


@web.route('/agreement')
def agreement():
    return '服务协议'


@web.route('/sdk')
def sdk():
    return 'SDK下载'
