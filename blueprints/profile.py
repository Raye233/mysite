from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import UserModel
from decorators import login_required
bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/user')
@login_required
def user():
    return render_template("personal.html")
