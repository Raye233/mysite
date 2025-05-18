from app import app
from redis_client import add_problem
import random


def generate_test_problems():
    difficulties = ["easy", "medium", "hard"]
    statuses = ["untried", "attempted", "solved"]
    des = ['题目描述样例1', '题目描述样例2']

    with app.app_context():  # 创建应用上下文
        for i in range(1, 50):
            title = f"Problem {i}"
            difficulty = random.choice(difficulties)
            status = random.choice(statuses)
            pass_rate = random.randint(10, 100)
            description = random.choice(des)

            add_problem(i, title, difficulty, status, pass_rate, description)
            print(
                f"Added problem {i}: {title}, Difficulty: {difficulty}, Status: {status}, Pass Rate: {pass_rate}%, Description: {description}")


if __name__ == '__main__':
    generate_test_problems()
