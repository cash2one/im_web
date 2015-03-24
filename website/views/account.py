# -*- coding: utf-8 -*-
from website.web import web
from website.blueprint_utils import login_required
from flask import request, g, render_template, redirect, url_for, session
from main.models.account import Account
from main.core import EmailUsageType


def get_user():
    user_id = session.get('user', {}).get('id')
    if user_id:
        account_obj = Account().set_id(user_id).find()
        return account_obj
    else:
        return {}


def update_session():
    result = get_user()
    if result:
        session['user']['id'] = result.get('id')
        session['user']['email'] = result.get('email')
        session['user']['email_checked'] = result.get('email_checked')
        session['user']['role'] = result.get('role')


@web.before_request
def before_request():
    g.uri_path = request.path
    if 'user' in session and session['user'].get('id'):
        if session['user'].get('email_checked') == 0:
            return redirect(url_for('web.register_valid'))
        else:
            # 已登录跳转到im主页
            if g.uri_path in ['/login', '/register']:
                return redirect(url_for('web.im_index'))


@web.route('/login')
def login():
    return render_template('user/login.html')


@web.route('/register')
def user_register():
    return render_template('user/register.html')


@web.route('/logout')
def logout():
    session['user'] = {}
    redirect_url = request.args.get('redirect_url')
    return redirect(url_for('.login', redirect_url=redirect_url))


@web.route('/register/valid')
def register_valid():
    code = request.args.get('code', '')
    error = ''
    if code:
        if 'user' in session:
            account_obj = get_user()
            confirm = account_obj.confirm_email(code, EmailUsageType.DEVELOPER_VERIFY)

            if confirm:
                account_obj.id = confirm['ro_id']
                account_obj.email = confirm['email']
                account_obj.email_checked = 1
                account_obj.save(['email_checked'])
                session['user']['email_checked'] = 1
                return redirect(url_for('.im_index'))
            else:
                error = '确认邮件失败'

    if 'user' in session and session['user'].get('access_token'):
        update_session()

    if 'user' in session and session['user'].get('email'):
        mail = session['user'].get('email')
        if session['user'].get('email_checked') == 1:
            return redirect(url_for('.im_index'))
    else:
        return redirect(url_for('.login'))

    if mail:
        suffix = mail.split('@')[1]
        suffix = suffix.lower()
        url = 'http://'
        if suffix == '163.com':
            url += 'mail.163.com'
        elif suffix == 'vip.163.com':
            url += 'vip.163.com'
        elif suffix == '126.com':
            url += 'mail.126.com'
        elif suffix == 'qq.com' or suffix == 'vip.qq.com' or suffix == 'foxmail.com':
            url += 'mail.qq.com'
        elif suffix == 'gmail.com':
            url += 'mail.google.com'
        elif suffix == 'sohu.com':
            url += 'mail.sohu.com'
        elif suffix == 'tom.com':
            url += 'mail.tom.com'
        elif suffix == 'vip.sina.com':
            url += 'vip.sina.com'
        elif suffix == 'sina.com.cn' or suffix == 'sina.com':
            url += 'mail.sina.com.cn'
        elif suffix == 'tom.com':
            url += 'mail.tom.com'
        elif suffix == 'yahoo.com.cn' or suffix == 'yahoo.cn':
            url += 'mail.cn.yahoo.com'
        elif suffix == 'tom.com':
            url += 'mail.tom.com'
        elif suffix == 'yeah.net':
            url += 'www.yeah.net'
        elif suffix == '21cn.com':
            url += 'mail.21cn.com'
        elif suffix == 'hotmail.com':
            url += 'www.hotmail.com'
        elif suffix == 'sogou.com':
            url += 'mail.sogou.com'
        elif suffix == '188.com':
            url += 'www.188.com'
        elif suffix == '139.com':
            url += 'mail.10086.cn'
        elif suffix == '189.cn':
            url += 'webmail15.189.cn/webmail'
        elif suffix == 'wo.com.cn':
            url += 'mail.wo.com.cn/smsmail'
        elif suffix == '139.com':
            url += 'mail.10086.cn'
        else:
            url = ''
    else:
        url = ''

    return render_template('user/register_valid.html', data={'mail': mail, 'redirect': url, 'error': error})


@web.route('/user/info')
@login_required
def user_info():
    """
    个人中心——基本资料
    """
    return render_template('user/info.html', data={'data': get_user()})


@web.route('/user/password')
@login_required
def user_password():
    """
    个人中心——修改密码
    """
    return render_template('user/password.html')


@web.route('/forget')
def password_forget():
    """
    忘记密码
    """
    return render_template('user/forget.html')


@web.route('/forget/valid')
def password_forget_check():
    """
    忘记密码——发送邮件
    """
    code = request.args.get('code', '')
    error = ''
    url = ''
    mail = request.args.get('mail', '')
    if mail:
        if 'user' not in session:
            session['user'] = {}
        session['user']['email'] = mail

    if code and mail:
        return render_template('user/reset_password.html', data={'code': code, 'mail': mail})

    if 'user' in session and session['user'].get('access_token'):
        update_session()

    if mail:
        suffix = mail.split('@')[1]
        suffix = suffix.lower()
        url = 'http://'
        if suffix == '163.com':
            url += 'mail.163.com'
        elif suffix == 'vip.163.com':
            url += 'vip.163.com'
        elif suffix == '126.com':
            url += 'mail.126.com'
        elif suffix == 'qq.com' or suffix == 'vip.qq.com' or suffix == 'foxmail.com':
            url += 'mail.qq.com'
        elif suffix == 'gmail.com':
            url += 'mail.google.com'
        elif suffix == 'sohu.com':
            url += 'mail.sohu.com'
        elif suffix == 'tom.com':
            url += 'mail.tom.com'
        elif suffix == 'vip.sina.com':
            url += 'vip.sina.com'
        elif suffix == 'sina.com.cn' or suffix == 'sina.com':
            url += 'mail.sina.com.cn'
        elif suffix == 'tom.com':
            url += 'mail.tom.com'
        elif suffix == 'yahoo.com.cn' or suffix == 'yahoo.cn':
            url += 'mail.cn.yahoo.com'
        elif suffix == 'tom.com':
            url += 'mail.tom.com'
        elif suffix == 'yeah.net':
            url += 'www.yeah.net'
        elif suffix == '21cn.com':
            url += 'mail.21cn.com'
        elif suffix == 'hotmail.com':
            url += 'www.hotmail.com'
        elif suffix == 'sogou.com':
            url += 'mail.sogou.com'
        elif suffix == '188.com':
            url += 'www.188.com'
        elif suffix == '139.com':
            url += 'mail.10086.cn'
        elif suffix == '189.cn':
            url += 'webmail15.189.cn/webmail'
        elif suffix == 'wo.com.cn':
            url += 'mail.wo.com.cn/smsmail'
        elif suffix == '139.com':
            url += 'mail.10086.cn'
        else:
            url = ''

    return render_template('user/forget_valid.html', data={'mail': mail, 'redirect': url, 'error': error})
