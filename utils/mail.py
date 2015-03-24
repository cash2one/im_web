# -*- coding: utf-8 -*-
"""使用
from flask import current_app
mail = current_app.extensions.get('mail')
mail.send_message("Hello",
              sender="from@example.com",
              recipients=["to@example.com"],
              body="testing",
              html = "<b>testing</b>")

如果设置了DEFAULT_MAIL_SENDER
mail.send_message("Hello",
              recipients=["to@example.com"],
              body="testing",
              html = "<b>testing</b>")

sender可以是tuple
mail.send_message("Hello",
              sender=("Me", "me@example.com"),
              body="testing",
              html = "<b>testing</b>")
"""
from flask.ext.mail import _Mail


class Mail(_Mail):

    @classmethod
    def init_app(cls, app):
        state = cls(
            app.config.get('MAIL_SERVER', 'smtp.exmail.qq.com'),
            app.config.get('MAIL_USERNAME', 'webmaster@gameservice.com'),
            app.config.get('MAIL_PASSWORD', 'ngpassw0rd'),
            app.config.get('MAIL_PORT', 465),
            app.config.get('MAIL_USE_TLS', False),
            app.config.get('MAIL_USE_SSL', True),
            app.config.get('MAIL_DEFAULT_SENDER', 'webmaster@gameservice.com'),
            int(app.config.get('MAIL_DEBUG', app.debug)),
            app.config.get('MAIL_MAX_EMAILS'),
            app.config.get('MAIL_SUPPRESS_SEND', app.testing))

        app.extensions = getattr(app, 'extensions', {})
        app.extensions['mail'] = state
        return state