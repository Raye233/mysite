from flask import Flask, render_template, request, session, g
from flask_migrate import Migrate
import config
from exts import db, mail
from models import UserModel
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from blueprints.profile import bp as profile_bp
import logging

app = Flask(__name__)
app.config.from_object(config)
logging.basicConfig(level=logging.WARNING)

db.init_app(app)
mail.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)

app.register_blueprint(profile_bp)

#  before_request/ before_first_request / after_request
@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)

#  上下文处理器，返回的数据在所有模板中有效
@app.context_processor
def my_context_processor():
    return {"user": g.user}


if __name__ == '__main__':
    app.run(debug=True)
