import redis

redis_conn = redis.Redis(host='localhost', port=6379)

def delete_all():
    for key in redis_conn.keys():
        redis_conn.delete(key)

def add():  # 哈希
    for idx in range(101, 106):
        redis_conn.hset("articles", str(idx), f"这是第{idx}篇文章")

def get_all():
    for article_id, article_title in redis_conn.hgetall("articles").items():
        print("#"*30)
        print(article_id, article_title)
        print(article_id.decode("utf-8"), article_title.decode("utf-8"))


if __name__ == '__main__':

    get_all()
    print(redis_conn.hget("articles", "104"))