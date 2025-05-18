import subprocess
import yaml
import time
from concurrent.futures import ThreadPoolExecutor


def run_code(code_path, input_data, timeout=2):
    """执行代码并返回输出和耗时（精确到毫秒）"""
    try:
        start_time = time.perf_counter()
        process = subprocess.run(
            ['python', code_path],
            input=str(input_data).encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout
        )
        end_time = time.perf_counter()

        stdout = process.stdout.decode().strip()
        stderr = process.stderr.decode().strip()
        duration = round((end_time - start_time) * 1000, 2)  # 转为毫秒

        if process.returncode != 0:
            return f"Runtime Error (exit code {process.returncode}): {stderr}", duration
        return stdout, duration
    except subprocess.TimeoutExpired:
        return "Time Limit Exceeded", timeout * 1000  # 转为毫秒
    except Exception as e:
        return f"Execution Error: {str(e)}", 0


def judge_test_case(problem_id, test_case, case_index):
    result = {
        'case_id': case_index + 1,
        'input': test_case.get('input', ''),
        'expected': test_case.get('output', ''),
        'actual': '',
        'status': 'Pending',
        'time_ms': 0,
        'is_passed': False
    }

    try:
        # 执行用户代码
        user_output, exec_time = run_code(
            f'submissions/{problem_id}.py',
            test_case['input']
        )

        # 执行参考答案
        ref_output, _ = run_code(
            f'code/{problem_id}.py',
            test_case['input']
        )

        # 记录结果
        result.update({
            'actual': user_output,
            'time_ms': exec_time,
            'is_passed': user_output == ref_output,
            'status': 'Accepted' if user_output == ref_output else
            'Time Limit Exceeded' if 'Time Limit Exceeded' in user_output else
            'Runtime Error' if 'Runtime Error' in user_output else
            'Wrong Answer'
        })

        # 特殊处理编译错误
        if 'SyntaxError' in user_output:
            result['status'] = 'Compile Error'

    except Exception as e:
        result['status'] = f'Judge System Error: {str(e)}'

    return result


def judge_code(problem_id):
    try:
        with open(f'test_cases/{problem_id}.yaml') as f:
            test_cases = yaml.safe_load(f) or []

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(judge_test_case, problem_id, tc, idx)
                       for idx, tc in enumerate(test_cases)]

            results = []
            total_time = 0
            for future in futures:
                case_result = future.result()
                results.append(case_result)
                total_time += case_result['time_ms']

            # 找出第一个错误用例
            failed_case = next((r for r in results if not r['is_passed']), None)

            return {
                'problem_id': problem_id,
                'total_cases': len(results),
                'passed_cases': sum(1 for r in results if r['is_passed']),
                'total_time_ms': round(total_time, 2),
                'details': results,
                'first_failed_case': failed_case
            }

    except FileNotFoundError:
        return {'error': 'Test cases not found'}
    except Exception as e:
        return {'error': f'Judge failed: {str(e)}'}