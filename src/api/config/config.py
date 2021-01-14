class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Production(Config):
    SQLALCHEMY_DATABASE_URI = '<Production DB URL>'


class Development(Config):
    # psql postgresql://Nghi:nghi1996@localhost/postgres
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://Nghi:nghi1996@localhost/postgres'
    SQLALCHEMY_ECHO = False
    JWT_SECRET_KEY = 'JWT_SECRET_NGHI!123'
    SECRET_KEY = 'SECRET_KEY_NGHI_ABC!123'
    SECURITY_PASSWORD_SALT = 'SECURITY_PASSWORD_SALT_NGHI_ABC!123'
    MAIL_DEFAULT_SENDER = 'dev2020@localhost'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'nghidev2020@gmail.com'
    MAIL_PASSWORD = 'nghi1996'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    UPLOAD_FOLDER = 'images'


class Testing(Config):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'postgresql://Nghi:nghi1996@localhost/postgres_test'
    SQLALCHEMY_ECHO = False
    JWT_SECRET_KEY = 'JWT_SECRET_NGHI!123'
    SECRET_KEY = 'SECRET_KEY_NGHI_ABC!123'
    SECURITY_PASSWORD_SALT = 'SECURITY_PASSWORD_SALT_NGHI_ABC!123'
    MAIL_DEFAULT_SENDER = 'dev2020@localhost'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'nghidev2020@gmail.com'
    MAIL_PASSWORD = 'nghi1996'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    UPLOAD_FOLDER = 'images'
