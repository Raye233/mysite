from flask import current_app
import redis

# 初始化 Redis 客户端
def init_redis(app):
    app.extensions['redis_client_verification'] = redis.StrictRedis(
        host=app.config['REDIS_HOST'],
        port=app.config['REDIS_PORT'],
        db=1,  # 验证码存储在数据库 1
        decode_responses=True
    )

    # 初始化题目 Redis 客户端
    app.extensions['redis_client_problems'] = redis.StrictRedis(
        host=app.config['REDIS_HOST'],
        port=app.config['REDIS_PORT'],
        db=0,  # 题目存储在数据库 0
        decode_responses=True
    )

def get_redis_client_verification():
    return current_app.extensions['redis_client_verification']

def get_redis_client_problems():
    return current_app.extensions['redis_client_problems']


def add_problem(problem_id, title, difficulty, status, pass_rate, description):
    redis_client = get_redis_client_problems()
    problem_key = f"problem:{problem_id}"

    if not redis_client.exists(problem_key):
        # 存储题目信息为哈希对象
        redis_client.hmset(problem_key, {
            "title": title,
            "difficulty": difficulty,
            "status": status,
            "pass_rate": pass_rate,
            "description": description
        })

    redis_client.zadd("problems", {problem_id: float(pass_rate)})