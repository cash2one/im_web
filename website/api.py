from flask import Blueprint, request, json, make_response, session, url_for
from main.models.account import Account
from main.core import RoleType, MainException, EmailUsageType, ResponseMeta
from blueprint_utils import login_required
from utils.func import init_logger
from config import APP_MODE

LOGGER = init_logger(__name__)

api = Blueprint('api', __name__, url_prefix='/api')


@api.errorhandler
def generic_error_handler(err):
    LOGGER.exception(err)
    return ResponseMeta(http_code=500, description='Server Internal Error!' if APP_MODE == 'Production' else str(err))


@api.route('/login', methods=['POST'])
def login_post():
    """
    """
    account_obj = _get_account_by_email(request.form.get('email', ''))
    if account_obj:
        if account_obj.check_password(request.form.get('password', '')):
            account = account_obj.present()
        else:
            raise MainException.ACCOUNT_PASSWORD_WRONG
    else:
        raise MainException.ACCOUNT_NOT_FOUND

    if 'user' not in session:
        session['user'] = {}

    if account:
        session['user']['name'] = account.get('name')
        session['user']['id'] = account.get('id')
        session['user']['email'] = account.get('email')
        session['user']['email_checked'] = account.get('email_checked')
        session['user']['role'] = account.get('role')
        session['user']['property'] = account.get('property')

    return send_response(account)


@api.route('/send_verify_email', methods=['POST'])
def verify_mail():
    """
    """
    account_obj = _get_account_by_email(request.form.get('email', ''))
    if account_obj:
        raise MainException.ACCOUNT_DUPLICATE

    account_obj = Account().init()
    if account_obj.feed(email=request.form.get('email', ''),
                        password=request.form.get('password', ''),
                        role=RoleType.DEVELOPER,
                        email_checked=0):
        account_obj.verify_email(email_cb=url_for('web.register_valid', code='', _external=True))

        account = account_obj.present()

        if 'user' not in session:
            session['user'] = {}

        if account:
            session['user']['id'] = account.get('id')
            session['user']['email'] = account.get('email')
            session['user']['email_checked'] = account.get('email_checked')
            session['user']['role'] = account.get('role')

        return send_response(account)


@api.route('/verify_email', methods=['POST'])
def verify_email():
    """
    """
    account_obj = _get_account()
    if not account_obj:
        raise MainException.ACCOUNT_NOT_FOUND

    if account_obj.email_checked:
        raise MainException.ACCOUNT_EMAIL_CHECKED

    account_obj.verify_email(url_for('web.register_valid', code='', _external=True))
    return MainException.OK


@api.route('/send_reset_email', methods=['POST'])
def reset_mail():
    """
    """
    email = request.form.get('email', '')

    if not email:
        raise MainException.ACCOUNT_NOT_FOUND

    account_obj = _get_account_by_email(email)
    if not account_obj:
        raise MainException.ACCOUNT_NOT_FOUND

    account_obj.forget_password(url_for('web.password_forget_check', mail=email, code='', _external=True))
    return MainException.OK


@api.route('/change_password', methods=['PUT'])
@login_required
def me_password():
    account = _get_account()

    if not account:
        raise MainException.ACCOUNT_NOT_FOUND

    if request.data:
        data = json.loads(request.data)

        if account.check_password(data.get('old_value')):
            account.password = data.get('new_value')
            account.save(['password'])
            return MainException.OK
        else:
            raise MainException.ACCOUNT_PASSWORD_WRONG
    else:
        raise MainException.ACCOUNT_PASSWORD_INVALID


@api.route('/reset_password', methods=['POST'])
def reset_password():
    if not request.data:
        raise MainException.ACCOUNT_PASSWORD_INVALID

    data = json.loads(request.data)
    code = data.get('code')
    password = data.get('password')

    if code:
        account_obj = Account()
        confirm = account_obj.confirm_email(code, EmailUsageType.DEVELOPER_RESET_PWD)
        # print confirm

        if confirm:
            account_obj.id = confirm['ro_id']
            account_obj.password = password
            account_obj.save(['password'])
            return MainException.OK

    raise MainException.ACCOUNT_INVALID_EMAIL_CODE


def _get_account():
    if 'user' in session:
        account_obj = Account().set_id(session['user']['id']).find()
        if not account_obj:
            raise None
        return account_obj
    else:
        return None


def _get_account_by_email(email):
    account_obj = Account()
    account_obj.email = email
    account_obj.role = RoleType.DEVELOPER
    accounts = account_obj.find()
    if accounts:
        return accounts[0]
    else:
        return None


def send_response(result):
    response = make_response(json.dumps(result))
    response.headers['Content-Type'] = 'application/json'

    return response

