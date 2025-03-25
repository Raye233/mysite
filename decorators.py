from functools import wraps
from flask import g, redirect, url_for

'''
@login_required
    def publish_question():
        pass
'''
def login_required(func):
    #  login_required保留func的信息
    @wraps(func)
    def inner(*args, **kwargs):
        #  判断g上是否有'user'属性
        if g.user:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('auth.login'))

    return inner
