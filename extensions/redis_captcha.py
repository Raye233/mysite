import redis
import random

redis_conn = redis.Redis(host='localhost', port=6379, db=0)


def generate_captcha(email):
    captcha = random.randint(1000, 9999)
    redis_key = f"captcha-{email}"
    # 将验证码存储到Redis中，键为"captcha:<email>"，值为验证码，过期时间为300秒（5分钟）
    redis_conn.set(redis_key, captcha, ex=300)
    return captcha

def verify_captcha(email, user_captcha):
    redis_key = f"captcha-{email}"
    stored_captcha = redis_conn.get(redis_key)
    print(stored_captcha, user_captcha)
    if stored_captcha and stored_captcha.decode('utf-8') == user_captcha:
        return True
    else:
        print("验证码验证失败")
        return False
