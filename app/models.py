from app import db
from flask_sqlalchemy.model import DefaultMeta

from abc import ABC

class Depts(ABC):
    LEVEL_1 = "level_1"
    LEVEL_2 = "level_2"
    LEVEL_3 = "level_3"



class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128),unique=True)
    password = db.Column(db.String(256))
    phone_no = db.Column(db.String(10),unique=True)
    first_name = db.Column(db.String(15),nullable=False)
    last_name = db.Column(db.String(15),nullable=False)
    dept = db.Column(db.String(100))

class Product(db.Model):
    id = db.Column(db.String(32),primary_key=True)
    notes = db.Column(db.String(140))
    verifier_depts = db.Column(db.String(255))
    created_by = db.Column(db.Integer,db.ForeignKey("users.id",ondelete="CASCADE"))
    verified_by = db.Column(db.Integer,db.ForeignKey("users.id",ondelete="CASCADE"),nullable=True)
    verified_at = db.Column(db.DateTime(),nullable=True)
    verifier_ip = db.Column(db.String(100),nullable=True)


