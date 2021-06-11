import random, yaml


SECRET_KEY = hex(random.getrandbits(64))[2:-1]

DB_INFO = yaml.load(open("db_info.yaml"), Loader=yaml.FullLoader)
SQLALCHEMY_DATABASE_URI = DB_INFO.get('uri')
SQLALCHEMY_TRACK_MODIFICATIONS = True

MAIL_INFO = yaml.load(open("mail_info.yaml"), Loader=yaml.FullLoader)
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = MAIL_INFO.get('username')
MAIL_PASSWORD = MAIL_INFO.get('password')