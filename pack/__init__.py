from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.secret_key = 'secret stuff'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:123@localhost/web'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
manager = LoginManager(app)

from pack import models, routes

db.create_all()
