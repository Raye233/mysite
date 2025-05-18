import os
from flask import Blueprint, render_template, request, flash, redirect, url_for, g
from sqlalchemy.sql.functions import current_user
from models import UserModel, QuestionModel, AnswerModel
from exts import db
from werkzeug.utils import secure_filename
from decorators import login_required
from werkzeug.security import generate_password_hash, check_password_hash
bp = Blueprint('profile', __name__, url_prefix='/profile')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@bp.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user(user_id):
    user = UserModel.query.get_or_404(user_id)
    if request.method == 'POST':
        if 'avatar' in request.files:
            file = request.files['avatar']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join('static', 'uploads', filename).replace(os.sep, '/')
                file.save(file_path)
                avatar_url = url_for('static', filename='uploads/' + filename)
                print(avatar_url)
                user.avatar = avatar_url
                db.session.commit()
                flash("头像已更新")
                return redirect(url_for('profile.user', user_id=user_id))
        user.username = request.form['username']
        password = request.form['password']
        if password:
            user.password = generate_password_hash(password)
        db.session.commit()
        flash("个人信息已更新")
        return redirect(url_for('profile.user', user_id=user_id))
    return render_template("personal.html", user=user)
