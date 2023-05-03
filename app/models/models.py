# coding:utf-8
from app import db


class User(db.Model):
    # 对应MySQL中数据表的名字
    __tablename__ = 'waimai_user'

    # 创建字段
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    user_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    head_img = db.Column(db.String(200))
    short_description = db.Column(db.String(300))
    email_hash = db.Column(db.String(300))
    user_level = db.Column(db.INTEGER,default=0)