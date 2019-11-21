from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_restplus import Api,Resource,fields,Namespace
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_script import Manager, Shell
from flask_mail import Mail, Message
import redis
api: Api = Api(
    title='Campus Guide',
    version='1.0',
    description='v1.0',
)
app = Flask(__name__)
app.config["SECRET_KEY"] = '765 PRODUCTION'
app.config.from_object(Config)
api.init_app(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

jwt = JWTManager(app)
CORS(app)
revoked_store = redis.StrictRedis(host='localhost', port=6379, db=0,
                                  decode_responses=True)
@jwt.token_in_blacklist_loader
def check_if_token_is_revoked(decrypted_token):
    jti = decrypted_token['jti']
    entry = revoked_store.get(jti)
    if entry is None:
        return True
    return entry == 'true'

if __name__ == '__main__':
    app.debug = True
    from authRoutes import api as ns1
    from postRoutes import api as ns2
    from commentRoutes import api as ns3
    from newsRoutes import api as ns4
    from courseRoutes import api as ns5

    api.add_namespace(ns1)
    api.add_namespace(ns2)
    api.add_namespace(ns3)
    api.add_namespace(ns4)
    api.add_namespace(ns5)

    app.run()
