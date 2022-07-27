from flask import Flask
from weddingapp import config
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_migrate import migrate
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
csrf = CSRFProtect(app)
db = SQLAlchemy(app)
from weddingapp.routes import user_routes,admin_routes
migrate = migrate(app,db)