import os


class Config:
    SECRET_KEY = "secret"
    SECURITY_PASSWORD_SALT = 'salt'
    #SECRET_KEY = os.environ.get('SECRET_KEY')
    #SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///chat.db'
    #SQLALCHEMY_BINDS = {
    #'chats': 'sqlite:///chat_databases/default_chat.db'  # Chat database
#}
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "luciislime69@gmail.com"
    MAIL_PASSWORD = "gibr ipfb etbw vbvl"
    MAIL_DEBUG = True
    MAIL_SUPPRESS_SEND = False

    #MAIL_USERNAME = os.environ.get('EMAIL_USER')
    #MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
