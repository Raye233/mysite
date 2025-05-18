from functools import wraps
from flask import g, redirect, url_for, request

def login_required(func):
    #  login_required保func的信息
    @wraps(func)
    def inner(*args, **kwargs):
        #  判断g上是否有'user'属性
        if g.user:
            return func(*args, **kwargs)
        else:
            next_url = request.url
            return redirect(url_for('auth.login', next=next_url))
    return inner
