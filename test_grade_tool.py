# -*- coding: utf-8 -*-
"""验收脚本：不依赖 pytest，用 print 逐条检查各函数的行为。

运行方式：python test_grade_tool.py
每条显示 [通过] 即表示该函数符合预期。
"""

from grade_tool import read_scores, average, max_score, count_failed
from grade_tool import DATA_FILE

print("=== 开始验收 ===")

# 测试 1：读文件（用项目里定义好的路径，不依赖你当前在哪个文件夹运行）
students = read_scores(DATA_FILE)
if students is not None and len(students) == 10:
    print("[通过] 测试1 读文件：读到 10 个学生")
    print("       第一个是", students[0])
else:
    print("[失败] 测试1 读文件：应该读到 10 个，实际", students)

# 测试 2：算平均分
avg = average([["张三", 80], ["李四", 90], ["王五", 100]])
if avg == 90:
    print("[通过] 测试2 平均分：80,90,100 的平均是 90")
else:
    print("[失败] 测试2 平均分：应该是 90，实际", avg)

# 测试 3：找最高分
mx = max_score([["张三", 80], ["李四", 100], ["王五", 90]])
if mx == 100:
    print("[通过] 测试3 最高分：找出 100")
else:
    print("[失败] 测试3 最高分：应该是 100，实际", mx)

# 测试 4：找最高分（全负数边界，防"擂主初始化为 0"的错）
mx2 = max_score([["A", -5], ["B", -2], ["C", -9]])
if mx2 == -2:
    print("[通过] 测试4 全负数最高分：找出 -2")
else:
    print("[失败] 测试4 全负数最高分：应该是 -2，实际", mx2)

# 测试 5：数不及格
failed = count_failed([["张三", 85], ["李四", 58], ["王五", 43], ["赵六", 90]])
if failed == 2:
    print("[通过] 测试5 不及格人数：85,58,43,90 里有 2 个不及格")
else:
    print("[失败] 测试5 不及格人数：应该是 2，实际", failed)

print("=== 验收结束 ===")
