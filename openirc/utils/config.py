import os


def init_config(app):
    if os.getenv('OPENIRC_CFG_ENV') is not None:
        load_environment(app)
    elif os.getenv('OPENIRC_CONFIG') is not None:
        app.config.from_envvar('OPENIRC_CONFIG')
    else:
        app.config.from_pyfile('../defaults.cfg')


def load_environment(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', None)
    app.config['TOKENIZER_SECRET_KEY'] = os.getenv('TOKENIZER_SECRET_KEY', None)
    app.config['TOKENIZER_SECURITY_PASSWORD_SALT'] = os.getenv('TOKENIZER_SECURITY_PASSWORD_SALT', None)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', None)
    app.config['SECURITY_PASSWORD_SALT'] = os.getenv('SECURITY_PASSWORD_SALT', None)
    app.config['WEB_LINK'] = os.getenv('WEB_LINK', None)
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', None)
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT', None)
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', None)
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', None)
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', None)
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', None)
    app.config['MAIL_DEBUG'] = os.getenv('MAIL_DEBUG', None)
    app.config['EMAIL_VERIFY'] = os.getenv('EMAIL_VERIFY', True)
