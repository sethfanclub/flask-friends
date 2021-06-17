import yaml, os


SECRET_KEY = os.environ.get('SECRET_KEY')

db_info = yaml.load(open("db_info.yaml"), Loader=yaml.FullLoader)
SQLALCHEMY_DATABASE_URI = db_info.get('uri')
SQLALCHEMY_TRACK_MODIFICATIONS = True

mail_info = yaml.load(open("mail_info.yaml"), Loader=yaml.FullLoader)
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = mail_info.get('username')
MAIL_PASSWORD = mail_info.get('password')