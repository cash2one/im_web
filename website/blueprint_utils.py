from functools import wraps
from flask import session, url_for, redirect


def login_required(function=None, redirect_url_for=None):
    def actual_decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user' in session and session['user'].get('access_token'):
                if session['user']['role'] == 1:
                    if session['user'].get('email_checked') == 0:
                        return redirect(url_for('web.register_valid'))
                    else:
                        return f(*args, **kwargs)
                elif session['user']['role'] == 2 or session['user']['role'] == 3:
                    return f(*args, **kwargs)

            return redirect(url_for('web.login',
                                    redirect_url=url_for(redirect_url_for)
                                    if redirect_url_for else None))

        return decorated_function

    if function:
        return actual_decorator(function)

    return actual_decorator
