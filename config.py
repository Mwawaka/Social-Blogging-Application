import os
# gets the base directory path of our application
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # retrieves the secret_key set in the environment variable
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SECURITY_PASSWORD_SALT=os.environ.get('SECURITY_PASSWORD_SALT')
    MAIL_SERVER = 'smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = '1e1c60de022d37'#os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = '369bea850420a3'#os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    FLASKY_MAIL_SUBJECT_PREFIX = ['Blogvolution']
    MAIL_DEFAULT_SENDER= os.environ.get('MAIL_DEFAULT_SENDER')
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    #os.environ.get('DEV_DATABASE_URL' or 'sqlite:///' +os.path.join(basedir,'development.db'))


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    # os.environ.get('TEST_DATABASE_URL')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///prod.db'
    # os.environ.get('PRODUCTION_DATABASE_URL')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
