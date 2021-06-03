import random, yaml


SECRET_KEY = hex(random.getrandbits(64))[2:-1]

db_info = yaml.load(open("db_info.yaml"))
SQLALCHEMY_DATABASE_URI = f'''mysql://
{db_info.get('username')}:
{db_info.get('password')}@
{db_info.get('host')}/
{db_info.get('database')}'''