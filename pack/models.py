from flask_login import UserMixin
from datetime import datetime

from pack import db, manager


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1024), nullable=False)
    user_cur = db.Column(db.String(16))

    def __init__(self, text, user_cur):
        self.text = text.strip()
        self.user_cur = user_cur.strip()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, title, intro, text):
        self.title = title.strip()
        self.intro = intro.strip()
        self.text = text.strip()


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
