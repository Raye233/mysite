# ACM模式：直接读取输入，处理后输出
import sys

for line in sys.stdin:
    try:
        a, b = map(int, line.strip().split())
        print(a - b)
    except:
        print("ERROR")

