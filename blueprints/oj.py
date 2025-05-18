import os
import subprocess
import traceback
from math import ceil
from flask import Blueprint, render_template, request, g, redirect, url_for, flash, jsonify
from redis_client import get_redis_client_problems
from decorators import login_required
from judge import *

bp = Blueprint('oj', __name__, url_prefix='/')


def get_problems(difficulty=None, status=None, sort=None, page_id=1, per_page=20):
    redis_client = get_redis_client_problems()
    problem_ids = redis_client.zrange("problems", 0, -1)  # 获取所有题目 ID

    if sort == 'id':
        problem_ids = sorted(problem_ids, key=lambda x: int(x))
    elif sort == 'pass_rate':
        problem_ids = sorted(
            problem_ids,
            key=lambda x: float(redis_client.hget(f"problem:{x}", "pass_rate")),
            reverse=True
        )
    else:
        # 默认按id升序
        problem_ids = sorted(problem_ids, key=lambda x: int(x))

    # 应用筛选条件
    filtered_problem_ids = []
    for problem_id in problem_ids:
        problem_key = f"problem:{problem_id}"
        problem_data = redis_client.hgetall(problem_key)

        if (not difficulty or problem_data.get("difficulty") == difficulty) and \
                (not status or problem_data.get("status") == status):
            filtered_problem_ids.append(problem_id)

    # 分页逻辑
    start = (page_id - 1) * per_page
    end = start + per_page
    paginated_problem_ids = filtered_problem_ids[start:end]

    problems = []
    for problem_id in paginated_problem_ids:
        problem_key = f"problem:{problem_id}"
        problem_data = redis_client.hgetall(problem_key)
        problems.append({
            "id": problem_id,
            "title": problem_data.get("title"),
            "difficulty": problem_data.get("difficulty", "unknown"),
            "status": problem_data.get("status", "untried"),
            "pass_rate": problem_data.get("pass_rate", "0")
        })

    return problems, len(filtered_problem_ids)

@bp.route('/problemset/', defaults={'page_id': 1})
@bp.route('/problemset/<int:page_id>')
@login_required
def problemset(page_id=1):
    page_id = max(page_id, 1)
    per_page = 20

    difficulty = request.args.get('difficulty', '')
    status = request.args.get('status', '')
    sort = request.args.get('sort', 'id')

    problems, total_problems = get_problems(difficulty, status, sort, page_id, per_page)
    total_pages = ceil(total_problems / per_page)

    if page_id > total_pages:
        return redirect(url_for('oj.problemset', page_id=total_pages))

    return render_template(
        "problemset.html",
        problems=problems,
        current_page=page_id,
        total_pages=total_pages,
        difficulty=difficulty,
        status=status,
        sort=sort
    )


@bp.route('/problemset/<int:problem_id>/description')
def problem_description(problem_id):
    return render_template("problem_description.html")  # 不再传递 problem_data


@bp.route('/api/problem/<int:problem_id>')
def get_problem_api(problem_id):
    redis_client = get_redis_client_problems()
    problem_data = redis_client.hgetall(f"problem:{problem_id}")

    if not problem_data:
        return jsonify({"error": "Problem not found"}), 404

    return jsonify({
        "title": problem_data.get("title", ""),
        "difficulty": problem_data.get("difficulty", "unknown"),
        "status": problem_data.get("status", "untried"),
        "pass_rate": problem_data.get("pass_rate", "0"),
        "description": problem_data.get("description", "")
    })


@bp.route('/api/total_problems')
def get_total_problems():
    redis_client = get_redis_client_problems()
    total = redis_client.zcard("problems")
    return jsonify({"total": total})


@bp.route('/submit', methods=['POST'])
def submit():
    try:
        # 验证请求数据
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "Empty request body"
            }), 400

        problem_id = data.get('problem_id')
        code = data.get('code')

        if not all([problem_id, code]):
            return jsonify({
                "success": False,
                "error": "Missing required fields"
            }), 400

        # 保存用户代码
        os.makedirs('submissions', exist_ok=True)
        try:
            with open(f'submissions/{problem_id}.py', 'w', encoding='utf-8') as f:
                f.write(code)
                print("成功写入代码")
        except IOError as e:
            return jsonify({
                "success": False,
                "error": f"Failed to save code: {str(e)}"
            }), 500

        # 执行判题
        results = judge_code(problem_id)
        print(results)
        return jsonify({
            "success": True,
            "results": results["details"],
            # "total_duration": results["total_duration"]
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
