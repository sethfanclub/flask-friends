import random, yaml


SECRET_KEY = hex(random.getrandbits(64))[2:-1]

DB_INFO = yaml.load(open("db_info.yaml"))
SQLALCHEMY_DATABASE_URI = DB_INFO.get('uri')