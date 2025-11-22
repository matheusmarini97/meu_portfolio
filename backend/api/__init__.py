from .handlers import registrar_error_handle
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask import Flask


app = Flask(__name__)
app.config.from_pyfile('config.py')
api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
registrar_error_handle(app)

from .namespaces import get_namespaces

for i in get_namespaces():
    api.add_namespace(i)