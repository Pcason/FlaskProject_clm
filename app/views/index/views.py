
import re

from datetime import datetime
from io import BytesIO
from flask import render_template, request, make_response, redirect, url_for, session, jsonify, current_app


from app import db, mail

from app.models.models import User
from . import index_blu
from app.utils.captcha import CreateCaptcha

login_time = ''


@index_blu.route('/login',methods=['GET', 'POST'])
@index_blu.route('/login.html', methods=['GET', 'POST'])
def login():
    global login_time
    if request.method == 'POST':
        phone = request.form.get('phone')
        password = request.form.get('password')
        # 获取返回数据的第一行
        obj = db.session.query(User).filter(User.phone == phone, User.password == password).first()
        if obj:
            response = make_response(redirect(url_for('.index')))
            session['login_flag'] = 'success'
            session['user_id'] = obj.user_id
            login_time = datetime.now()
            return jsonify({'errmsg':'登陆成功', 'statu':0})

        else:
            # response.set_cookie('login_flag', 'error')
            return jsonify({'errmsg':'用户名或密码错误', 'statu':1})

    elif request.method == 'GET':
        return render_template('index/login.html')


@index_blu.route('/register', methods=['GET', 'POST'])
@index_blu.route('/register.html', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('index/register.html')
    elif request.method == 'POST':
        print(request.form)
        user_name = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        password1 = request.form.get('password1')
        checkcode = request.form.get('checkcode')
        code_text = session.get('code_text')
        # print(user_name)
        if not (user_name and email and password and checkcode and phone):
            ret = {
                'status': 2,
                'errmsg': '请输入完整信息!'
            }
            return jsonify(ret)
        elif not re.match(r"\w+[@][a-zA-Z0-9_]+(\.[a-zA-Z0-9_]+)+", email):
            ret = {
                'status': 3,
                'errmsg': '邮箱格式错误!'
            }
            return jsonify(ret)
        elif password != password1:
            ret = {
                'status': 4,
                'errmsg': '两次密码不一致!'
            }
            return jsonify(ret)
        elif checkcode.lower() != code_text.lower():
            ret = {
                'status': 5,
                'errmsg': '验证码错误!'
            }
            session['code_text'] = ''
            return jsonify(ret)
        else:
            # 创建session对象
            # DBSession = sessionmaker(bind=engine)  # 创建与数据库的会话，返回的是一个类
            # db_session = DBSession()  # 生成链接数据库的实例
            # 获取返回数据的第一行
            obj = db.session.query(User).filter(db.or_(User.user_name == user_name, User.phone == phone)).first()
            # 关闭session

            if obj:
                ret = {
                    'status': 1,
                    'errmsg': '账号已存在!'
                }
                return jsonify(ret)
            else:
                ret = {
                    'status': 0,
                    'errmsg': '注册成功'
                }
                user_id = email[:email.find("@")]
                new_user = User(user_id=user_id, user_name=user_name, email=email, phone=phone, password=password)
                db.session.add(new_user)
                db.session.commit()
                # email_hash = hashlib.md5()
                # email_hash.update(str(time.time()).encode('utf-8'))
                # email_value = email_hash.hexdigest()
                # email_verify = request.host_url + 'verify_mail?email_hash=' + email_value
                # msg = Message('欢迎注册吃了么网站', sender='xaingyun888@163.com', recipients=[email])
                # # 这里的sender是发信人，写上你发信人的名字，比如张三。
                # # recipients是收信人，用一个列表去表示。
                # msg.body = '你好'
                # msg.html = f'点击<a href="{email_verify}">验证</a>邮箱，开启吃了么网站之旅！'
                # mail.send(msg)
                # new_user.email_hash = email_value
                # db.session.add(new_user)
                # db.session.commit()
                return jsonify(ret)


@index_blu.route('/captcha')
def captcha():
    creat_code = CreateCaptcha()
    image, code_text = creat_code.gen_code()
    buf = BytesIO()
    image.save(buf, 'png')
    image_data = buf.getvalue()
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/png'
    session['code_text'] = code_text
    # print(code_text)
    return response


@index_blu.route('/')
@index_blu.route('/index')
@index_blu.route('/index.html')
def index():
    login_flag = session.get('login_flag')
    user_id = session.get('user_id')
    if login_flag == 'success' and session.get('user_id'):
        # 1. 查询数据库
        # 创建session对象
        # DBSession = sessionmaker(bind=engine)  # 创建与数据库的会话，返回的是一个类
        # db_session = DBSession()  # 生成链接数据库的实例

        # 获取返回数据的第一行
        obj = db.session.query(User).filter(User.user_id == str(user_id)).first()
        # 关闭session
        # db_session.close()

        # 2. 模板渲染
        return render_template("index/index.html", username='欢迎您！ ' + obj.user_name)
    return render_template('index/index.html')


@index_blu.route('/article_list.html')
def article_list():
    return render_template('index/article_list.html')


@index_blu.route('/article_read.html')
def article_read():
    return render_template('index/article_read.html')


@index_blu.route('/cart.html')
def cart():
    if request.args.get('Number'):
        number = request.args.get('Number')
        # print(number)
        return render_template('index/cart.html', number=number)
    return render_template('index/cart.html')


@index_blu.route('/category.html')
def category():
    return render_template('index/category.html')


@index_blu.route('/confirm_order.html')
def confirm_order():
    login_flag = session.get('login_flag')
    user_id = session.get('user_id')
    if login_flag == 'success' and session.get('user_id'):
        # 1. 查询数据库
        # 创建session对象
        # DBSession = sessionmaker(bind=engine)  # 创建与数据库的会话，返回的是一个类
        # db_session = DBSession()  # 生成链接数据库的实例

        # 获取返回数据的第一行
        obj = db.session.query(User).filter(User.user_id == str(user_id)).first()
        # 关闭session
        # db_session.close()

        # 2. 模板渲染
        return render_template("index/confirm_order.html", username='欢迎您！ ' + obj.user_name)
    return redirect(url_for('.login'))


@index_blu.route('/logout')
def logout():
    response = make_response(redirect(url_for('.index')))
    session.clear()
    return response


@index_blu.route('/detailsp.html')
def detailsp():
    return render_template('index/detailsp.html')


@index_blu.route('/error.html')
def error():
    return render_template('index/error.html')


@index_blu.route('/list.html')
def list():
    return render_template('index/list.html')


@index_blu.route('/reserve.html')
def reserve():
    return render_template('index/reserve.html')


@index_blu.route('/respond.html')
def respond():
    return render_template('index/respond.html')


@index_blu.route('/search_p.html')
def search_p():
    return render_template('index/search_p.html')


@index_blu.route('/search_s.html')
def search_s():
    return render_template('index/search_s.html')


@index_blu.route('/shop.html')
def shop():
    return render_template('index/shop.html')


@index_blu.route('/shop2.html')
def shop2():
    return render_template('index/shop2.html')

@index_blu.route('/user_account',methods=['GET', 'POST'])
@index_blu.route('/user_account.html',methods=['GET', 'POST'])
def user_account():
    if request.method == 'GET':
        login_flag = session.get('login_flag')
        user_id = session.get('user_id')
        if login_flag == 'success' and session.get('user_id'):
            # 1. 查询数据库
            # 创建session对象
            # DBSession = sessionmaker(bind=engine)  # 创建与数据库的会话，返回的是一个类
            # db_session = DBSession()  # 生成链接数据库的实例

            # 获取返回数据的第一行
            obj = db.session.query(User).filter(User.user_id == str(user_id)).first()
            # 关闭session
            # db_session.close()

            # 2. 模板渲染
            return render_template("index/user_account.html", username='欢迎您！ ' + obj.user_name, email=obj.email,
                                   phone=obj.phone)
        return redirect(url_for('.login'))
    elif request.method == 'POST':
        user_name = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        old_phone =request.form.get('old_phone')
        # print(old_phone)
        if user_name and email and phone:
            obj = db.session.query(User).filter(User.phone == str(old_phone)).first()
            # print(obj)
            obj.user_name = user_name
            obj.email = email
            obj.phone = phone
            db.session.commit()
            ret = {
                'status': 0,
                'errmsg': '保存成功!'
            }
            return jsonify(ret)
        else:
            ret = {
                'status': 1,
                'errmsg': '请填写完整信息！'
            }
            return jsonify(ret)


@index_blu.route('/user_address.html')
def user_address():
    login_flag = session.get('login_flag')
    user_id = session.get('user_id')
    if login_flag == 'success' and session.get('user_id'):
        # 1. 查询数据库
        # 创建session对象
        # DBSession = sessionmaker(bind=engine)  # 创建与数据库的会话，返回的是一个类
        # db_session = DBSession()  # 生成链接数据库的实例

        # 获取返回数据的第一行
        obj = db.session.query(User).filter(User.user_id == str(user_id)).first()
        # 关闭session
        # db_session.close()

        # 2. 模板渲染
        return render_template("index/user_address.html", username='欢迎您！ ' + obj.user_name)
    return redirect(url_for('.login'))


@index_blu.route('/user_center.html')
def user_center():
    login_flag = session.get('login_flag')
    user_id = session.get('user_id')
    if login_flag == 'success' and session.get('user_id'):
        # 1. 查询数据库
        # 创建session对象
        # DBSession = sessionmaker(bind=engine)  # 创建与数据库的会话，返回的是一个类
        # db_session = DBSession()  # 生成链接数据库的实例

        # 获取返回数据的第一行
        obj = db.session.query(User).filter(User.user_id == str(user_id)).first()
        # 关闭session
        # db_session.close()

        # 2. 模板渲染
        return render_template("index/user_center.html", username='欢迎您！ ' + obj.user_name,
                               login_time=str(login_time).split('.')[0])
    return redirect(url_for('.login'))


@index_blu.route('/user_coupon.html')
def user_coupon():
    login_flag = session.get('login_flag')
    user_id = session.get('user_id')
    if login_flag == 'success' and session.get('user_id'):
        # 1. 查询数据库
        # 创建session对象
        # DBSession = sessionmaker(bind=engine)  # 创建与数据库的会话，返回的是一个类
        # db_session = DBSession()  # 生成链接数据库的实例

        # 获取返回数据的第一行
        obj = db.session.query(User).filter(User.user_id == str(user_id)).first()
        # 关闭session
        # db_session.close()

        # 2. 模板渲染
        return render_template("index/user_coupon.html", username='欢迎您！ ' + obj.user_name)
    return redirect(url_for('.login'))


@index_blu.route('/user_favorites.html')
def user_favorites():
    login_flag = session.get('login_flag')
    user_id = session.get('user_id')
    if login_flag == 'success' and session.get('user_id'):
        # 1. 查询数据库
        # 创建session对象
        # DBSession = sessionmaker(bind=engine)  # 创建与数据库的会话，返回的是一个类
        # db_session = DBSession()  # 生成链接数据库的实例

        # 获取返回数据的第一行
        obj = db.session.query(User).filter(User.user_id == str(user_id)).first()
        # 关闭session
        # db_session.close()

        # 2. 模板渲染
        return render_template("index/user_favorites.html", username='欢迎您！ ' + obj.user_name)
    return redirect(url_for('.login'))


@index_blu.route('/user_message.html')
def user_message():
    login_flag = session.get('login_flag')
    user_id = session.get('user_id')
    if login_flag == 'success' and session.get('user_id'):
        # 1. 查询数据库
        # 创建session对象
        # DBSession = sessionmaker(bind=engine)  # 创建与数据库的会话，返回的是一个类
        # db_session = DBSession()  # 生成链接数据库的实例

        # 获取返回数据的第一行
        obj = db.session.query(User).filter(User.user_id == str(user_id)).first()
        # 关闭session
        # db_session.close()

        # 2. 模板渲染
        return render_template("index/user_message.html", username='欢迎您！ ' + obj.user_name)
    return redirect(url_for('.login'))


@index_blu.route('/user_order.html')
def user_order():
    login_flag = session.get('login_flag')
    user_id = session.get('user_id')
    if login_flag == 'success' and session.get('user_id'):
        # 1. 查询数据库
        # 创建session对象
        # DBSession = sessionmaker(bind=engine)  # 创建与数据库的会话，返回的是一个类
        # db_session = DBSession()  # 生成链接数据库的实例

        # 获取返回数据的第一行
        obj = db.session.query(User).filter(User.user_id == str(user_id)).first()
        # 关闭session
        # db_session.close()

        # 2. 模板渲染
        return render_template("index/user_order.html", username='欢迎您！ ' + obj.user_name)
    return redirect(url_for('.login'))


@index_blu.route('/user_orderlist.html')
def user_orderlist():
    login_flag = session.get('login_flag')
    user_id = session.get('user_id')
    if login_flag == 'success' and session.get('user_id'):
        # 1. 查询数据库
        # 创建session对象
        # DBSession = sessionmaker(bind=engine)  # 创建与数据库的会话，返回的是一个类
        # db_session = DBSession()  # 生成链接数据库的实例

        # 获取返回数据的第一行
        obj = db.session.query(User).filter(User.user_id == str(user_id)).first()
        # 关闭session
        # db_session.close()

        # 2. 模板渲染
        return render_template("index/user_orderlist.html", username='欢迎您！ ' + obj.user_name)
    return redirect(url_for('.login'))

