import os
import configparser
import datetime
import pytz 


cfg = configparser.ConfigParser()
cfg.read('./env-stag.ini')


REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_PASS = os.getenv("REDIS_PASS", "password")
REDIS_DB = os.getenv("REDIS_DB_BACKEND", "0")

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "broker")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", "5672")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
RABBITMQ_VHOST = os.getenv("RABBITMQ_VHOST", "")


# RabbitMQ connection string: amqp://user:pass@localhost:5672/myvhost
BROKER = "amqp://{userpass}{hostname}{port}{vhost}".format(
    hostname=RABBITMQ_HOST,
    userpass=RABBITMQ_USER + ":" + RABBITMQ_PASS + "@" if RABBITMQ_USER else "",
    port=":" + RABBITMQ_PORT if RABBITMQ_PORT else "",
    vhost="/" + RABBITMQ_VHOST if RABBITMQ_VHOST else ""
)

REDIS_BACKEND = "redis://{password}{hostname}{port}{db}".format(
    hostname=REDIS_HOST,
    password=':' + REDIS_PASS + '@' if REDIS_PASS else '',
    port=":" + REDIS_PORT if REDIS_PORT else "",
    db="/" + REDIS_DB if REDIS_DB else ""
)


#=========================================================================
#                           TIMING CONFIG
#=========================================================================
u = datetime.datetime.utcnow()
u = u.replace(tzinfo=pytz.timezone("Asia/Ho_Chi_Minh"))


#=========================================================================
#                          PROJECT INFORMATION 
#=========================================================================
PROJECT = cfg['project']
PROJECT_NAME = PROJECT['name']
ENVIRONMENT = PROJECT['environment']
HOST_NAME = PROJECT['host_name']


BACKEND = cfg['backend']
BE_PORT = BACKEND.getint('port')
FRONTEND = cfg['frontend']
FE_PORT = FRONTEND.getint('port')


#=========================================================================
#                          DATABASE INFORMATION 
#=========================================================================
DATABASE = cfg['database']
SQLALCHEMY_DATABASE_URL = "{type}://{user}:{pw}@{host}:{port}/{db_name}" \
    .format(
        type = DATABASE['type'],
        user = DATABASE['user'],
        pw = DATABASE['pass'],
        host = DATABASE['host'],
        port = DATABASE['port'],
        db_name = DATABASE['database'],
    )
DATABASE_SCHEMA = DATABASE['schema']


#=========================================================================
#                          AUTHENTICATE INFORMATION 
#=========================================================================
AUTHENTICATE = cfg['authenticate']
ENCODE_TYPE = AUTHENTICATE['encode']
DIGEST = AUTHENTICATE['digest']    
ALGORITHM = AUTHENTICATE['algorithm']
ROUNDS = AUTHENTICATE.getint('rounds')
SALT_SIZE = AUTHENTICATE.getint('salt_size')
SALT = bytes(AUTHENTICATE['salt'], "utf-8").decode('unicode_escape')
ACCESS_TOKEN_EXPIRE_MINUTES = AUTHENTICATE.getint('access_expire')
FRESH_TOKEN_EXPIRE_MINUTES = AUTHENTICATE.getint('fresh_expire')
SECRET_KEY = AUTHENTICATE['secret_key']


#=========================================================================
#                          NAS INFORMATION 
#=========================================================================
NAS = cfg['nas']
NAS_HOST = NAS['host']
NAS_USER = NAS['user']
NAS_PASSWORD = NAS['pass']
NAS_CERT_PATH = NAS['cert_path']
NAS_ROOT_PATH = NAS['root_path']


AIRFLOW_API_ENDPOINT = "https://dwh-staging-etl.digi-texx.vn/airflow/api/experimental"  


#=========================================================================
#                          LDAP INFORMATION 
#=========================================================================
LDAP = cfg['ldap']
LDAP_SERVER = LDAP['server']
LDAP_BASE = LDAP['base']
LDAP_ROOT_DN = LDAP['root_dn']
LDAP_ADMIN_USER = LDAP['admin_user']
LDAP_ADMIN_PASSWORD = LDAP['admin_password']