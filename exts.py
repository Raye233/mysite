# 为了解决循环应用
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message


db = SQLAlchemy()
mail = Mail()