# coding:utf-8
class Config(object):
    """项目的配置类"""

    SECRET_KEY = "1"
    # 数据库相关配置
    # 设置数据库的链接地址
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:python@localhost:3306/flask1?charset=utf8'
    # 关闭追踪数据库的修改
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """开发环境中的配置类"""
    # 开启调试模式
    # DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:222325938PRB@localhost:3306/flask1?charset=utf8'
    MAIL_SERVER = 'smtp.163.com'  # 电子邮件服务器的主机名或IP地址
    MAIL_PORT = 25  # 电子邮件服务器的端口
    MAIL_USE_TLS = True  # 启用传输层安全
    # 注意这里启用的是TLS协议(transport layer security)，而不是SSL协议所以用的是25号端口
    MAIL_USERNAME = 'xaingyun888@163.com'  # 你的邮件账户用户名
    MAIL_PASSWORD = 'ZBXDNJCXVVFKYXNB'  # 邮件账户的密码,这个密码是指的授权码!授权码!授权码!


class ProductionConfig(Config):
    """生产环境(线上)中配置类"""
    # 配置生产环境中使用的配置类
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:xxxxxx@localhost:3306/flask_1?charset=utf8'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:222325938PRB@123.249.7.225:3306/flask?charset=utf8'


APPCONFIG = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
