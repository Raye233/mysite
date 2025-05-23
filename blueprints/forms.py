import wtforms
from wtforms.validators import Email, Length, EqualTo, InputRequired
from models import UserModel
from redis_captcha import *

class RegistrationForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误!")])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="验证码格式错误!")])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message="用户名格式错误!")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误!")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="两次密码不一致!")])

    #  自定义验证
    # 1， 邮箱是否已经被注册
    def validate_email(self, field):  # validate_xxxx为固定写法
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="该邮箱已经被注册!")

    # 2， 验证码是否正确
    # def validate_captcha(self, field):
    #     captcha = field.data
    #     email = self.email.data
    #     captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
    #     if not captcha_model:
    #         raise wtforms.ValidationError(message="邮箱或验证码错误!")

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        print(captcha)
        if not verify_captcha(email, captcha):
            raise wtforms.ValidationError(message="邮箱或验证码错误!")


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误!")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误!")])

class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=3, max=100, message="标题格式错误!")])
    content = wtforms.StringField(validators=[Length(min=3, message="内容格式错误!")])

class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=3, message="内容格式错误!")])
    question_id = wtforms.IntegerField(validators=[InputRequired(message="必须传入问题id!")])

class ProfileForm(wtforms.Form):
    nickname = wtforms.StringField(validators=[Length(min=3, message="昵称格式错误!")])
    age = wtforms.StringField(validators=[Length(min=0, max=2, message="年龄格式错误!")])
    area = wtforms.StringField(validators=[Length(min=0, max=20, message="地区格式错误!")])
    self_introduction = content = wtforms.StringField(validators=[Length(min=3, message="内容格式错误!")])

class RetrieveForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误!")])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="验证码格式错误!")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误!")])

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        print(captcha)
        if not verify_captcha(email, captcha):
            raise wtforms.ValidationError(message="邮箱或验证码错误!")