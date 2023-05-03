# coding:utf-8
from flask import Flask, render_template
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from config import APPCONFIG

db = SQLAlchemy()
mail = Mail()


def create_app(config_name):
    app = Flask(__name__)
    # 设置session秘钥
    app.config['SECRET_KEY'] = '123456'
    from app.views.admin import admin_blu
    from app.views.index import index_blu
    # 注册蓝图
    app.register_blueprint(admin_blu, url_prefix='/admin')
    app.register_blueprint(index_blu)
    # 数据库相关配置
    # 设置数据库的链接地址
    # app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:222325938PRB@localhost:3306/flask1?charset=utf8'
    # # 关闭追踪数据库的修改
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config.from_object(APPCONFIG.get(config_name))
    db.init_app(app)
    mail.init_app(app)

    # 配置404
    @app.errorhandler(404)
    def error_404(e):
        return render_template('index/error.html'), 404

    return app
