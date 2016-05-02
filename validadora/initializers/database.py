from flask.ext.mongoengine import MongoEngine
from validadora.proxy import Proxy as proxy
import os

MONGO_PORT = os.getenv("MONGO_PORT_27017_TCP_PORT", 27017)
MONGO_ADDR = os.getenv('MONGO_PORT_27017_TCP_ADDR', '127.0.0.1')
MONGO_DB = os.getenv('MONGO_DATABASE', 'validadora_dev')
MONGO_USER = os.getenv('MONGO_USER', False)
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD', False)

def initialize_db(app):
    db = MongoEngine()
    app.config['MONGODB_SETTINGS'] = {}

    if MONGO_PASSWORD:
        app.config['password'] = MONGO_PASSWORD

    if MONGO_USER:
        app.config['username'] = MONGO_USER

    if MONGO_ADDR:
        app.config['host'] = MONGO_ADDR

    if MONGO_PORT:
        app.config['port'] = int(MONGO_PORT)

    if MONGO_DB:
        app.config['db'] = MONGO_DB

    db.init_app(app)
    proxy.db = db
    return db