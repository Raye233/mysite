from flask import Blueprint, render_template, jsonify, redirect, url_for, request, session, flash
from pyexpat.errors import messages
from flask import request
from exts import mail, db
from flask_mail import Message
import random
from models import EmailCaptchaModel, UserModel
from .forms import RegistrationForm, LoginForm, RetrieveForm
from werkzeug.security import generate_password_hash, check_password_hash
from extensions.redis_captcha import *
# /auth
bp = Blueprint("auth", __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                flash('该邮箱未注册。', 'error')
                print("邮箱在数据中不存在!")
                return redirect(url_for('auth.login'))
            if check_password_hash(user.password, password):
                #  flask中的session,是经过加密后存储在session中的
                session['user_id'] = user.id
                return redirect("/")
            else:
                flash('密码错误，请重试。', 'error')
                print("密码错误!")
                return redirect(url_for('auth.login'))
        else:
            print(form.errors)
            return redirect(url_for('auth.login'))


#  通过mysql存储验证码并比对
# @bp.route('/captcha/email')
# def get_email_captcha():
#     email = request.args.get("email")
#     captcha = random.randint(1000, 9999)
#     message = Message(subject="注册验证码", recipients=[email], body=f"您的验证码是:{captcha}")
#     mail.send(message)
#     email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
#     db.session.add(email_captcha)
#     db.session.commit()
#     return jsonify({"code": 200, "message": "", "data": None})

# @bp.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'GET':
#         return render_template("register.html")
#     else:
#         form = RegistrationForm(request.form)
#         if form.validate():
#             email = form.email.data
#             username = form.username.data
#             password = form.password.data
#             user = UserModel(email=email, username=username, password=generate_password_hash(password))
#             db.session.add(user)
#             db.session.commit()
#             return redirect(url_for('auth.login'))
#         else:
#             print(form.errors)
#             return redirect(url_for('auth.register'))

@bp.route('/captcha/email')
def get_email_captcha():
    email = request.args.get("email")
    captcha = generate_captcha(email)
    message = Message(subject="邮箱验证码", recipients=[email], body=f"您的验证码是:{captcha}")
    mail.send(message)
    return jsonify({"code": 200, "message": "", "data": None})

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        form = RegistrationForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            flash('信息填写不一致或错误，请重试。', 'error')
            print(form.errors)
            return redirect(url_for('auth.register'))

@bp.route('/retrieve', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
        return render_template('retrieve.html')
    else:
        form = RetrieveForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            user.password = generate_password_hash(password)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            print(form.errors)
            return redirect(url_for('auth.forgot_password'))


@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@bp.route('/mail/test')
def mail_test():
    message = Message(subject="test", recipients=["3272297930@qq.com"], body="这是一条测试邮件!")
    mail.send(message)
    return "邮件发送成功!"
