import os

from cffi.backend_ctypes import unicode
from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask.json import JSONEncoder

from conf import Config


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        from speaklater import is_lazy_string
        if is_lazy_string(obj):
            try:
                return unicode(obj)
            except NameError:
                return str(obj)
        return super(CustomJSONEncoder, self).default(obj)


app = Flask(__name__, static_url_path='')
app.config.from_object(Config)
app.secret_key = os.getenv("SECRET_KEY")

login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)

app.json_encoder = CustomJSONEncoder

db = SQLAlchemy(app=app)
ma = Marshmallow(app)
db.create_all()
from app import routes, models
