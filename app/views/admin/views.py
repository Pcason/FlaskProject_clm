# coding:utf-8
from flask import render_template, request, make_response, redirect, url_for, session, jsonify, current_app
from app import db
from app.models.models import User
from . import admin_blu


@admin_blu.route('/index')
@admin_blu.route('/index.html')
def index():
    login_flag= request.cookies.get('login_flag')
    user_id = request.cookies.get('user_id')
    if  login_flag == 'success' and user_id == '123456':
        page_size = 7  # 每页10个
        page = request.args.get('page')
        if page:
            page_index = page
        else:
            page_index = 2  # 查询的是第几页开始(从1开始计算)
        paginate = db.session.query(User).paginate(page=int(page_index), per_page=int(page_size), error_out=False)
        # 遍历时要加上items
        users = paginate.items
        return render_template('admin/admin.html', users=users, paginate=paginate)
    else:
        return redirect(url_for('.login'))


@admin_blu.route('/')
@admin_blu.route('/login')
def login():
    if request.args:
        user_name = request.args.get('username')
        password = request.args.get('Password')

        if user_name == 'admin' and password == "123456":
            response = make_response(redirect(url_for('.index')))
            response.set_cookie('login_flag', 'success')
            response.set_cookie('user_id', '123456')
            return response

        else:
            return '登录失败,用户名或密码错误!'

    else:
        return render_template('admin/login.html')
