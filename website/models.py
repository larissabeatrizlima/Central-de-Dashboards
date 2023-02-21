from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Link = db.Column(db.String(1000000))
    Dashboard = db.Column(db.String(10000))
    Segmento = db.Column(db.String(10000))
    Permissao = db.Column(db.Integer,db.ForeignKey('user.Permissao'))
    user_id = db.Column(db.Integer)
    


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    Senha = db.Column(db.String(150))
    Permissao = db.Column(db.String(150))
    notes = db.relationship('Note')
