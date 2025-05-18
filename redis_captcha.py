import random
from redis_client import get_redis_client_verification


def generate_captcha(email):
    redis_conn = get_redis_client_verification()
    captcha = random.randint(1000, 9999)
    redis_key = f"captcha-{email}"
    # 将验证码存储到Redis中，键为"captcha:<email>"，值为验证码，过期时间为300秒（5分钟）
    redis_conn.set(redis_key, captcha, ex=300)
    return captcha

def verify_captcha(email, user_captcha):
    redis_conn = get_redis_client_verification()
    redis_key = f"captcha-{email}"
    stored_captcha = redis_conn.get(redis_key)
    print(stored_captcha, user_captcha)
    if stored_captcha and stored_captcha == str(user_captcha):
        redis_conn.delete(redis_key)  # 验证成功后删除验证码
        return True
    else:
        print("验证码验证失败")
        return False
