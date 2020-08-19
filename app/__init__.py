import os

from cffi.backend_ctypes import unicode
from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
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
app.secret_key = 'LLucNgKPMEJ4JXZrCXx3YgrH'

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.refresh_view = 'login'
login_manager.needs_refresh_message = (u"Session timedout, please re-login")
login_manager.needs_refresh_message_category = "info"
login_manager.init_app(app)
bcrypt = Bcrypt(app)

app.json_encoder = CustomJSONEncoder

db = SQLAlchemy(app=app)
db.create_all()
from app import routes, models
