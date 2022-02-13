from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import os
from . import parsers

app = Flask(__name__)
app.config.from_object(os.environ.get('FLASK_ENV') or 'config.TestingConfig')
app.config.from_object('config.TestingConfig')
app.config['BUNDLE_ERRORS'] = True
api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.session_protection = 'basic'

from . import views
