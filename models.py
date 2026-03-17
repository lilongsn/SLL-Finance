from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    # 预算设置
    monthly_budget = db.Column(db.Float, default=0.0)
    transactions = db.relationship("Transaction", backref="owner", lazy=True)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    type = db.Column(db.String(10), nullable=False)  # '支出' 或 '收入'
    category_main = db.Column(db.String(50), nullable=False)  # 一级分类
    category_sub = db.Column(db.String(50))  # 二级分类
    note = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
