import eventlet
from eventlet import wsgi
from flask import Flask, render_template, request, session, g
from flask_migrate import Migrate
import config
from exts import db, mail
from models import UserModel
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from blueprints.profile import bp as profile_bp
from blueprints.oj import bp as oj_bp
import logging
from redis_client import init_redis
from flask_cors import CORS
import logging
from waitress import serve

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)  # 允许跨域请求

app.config.from_object(config)

db.init_app(app)
mail.init_app(app)

init_redis(app)

migrate = Migrate(app, db)

app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(oj_bp)


#  before_request/ before_first_request / after_request
@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        # user = UserModel.query.get(user_id)
        user = db.session.get(UserModel, user_id)
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)


#  上下文处理器，返回的数据在所有模板中有效
@app.context_processor
def my_context_processor():
    return {"user": g.user}


if __name__ == '__main__':
    app.run(threaded=True, debug=False, port=5000)
    # serve(app, host='0.0.0.0', port=5000)
