# -*- coding: utf-8 -*-
"""
成绩统计小工具

从 data/scores.txt 读取学生成绩，计算平均分、最高分和不及格人数，
结果打印到终端，同时写入 output/report.txt。

只依赖 Python 标准库（os）。文件路径以脚本位置为基准计算，
因此从任何工作目录运行都能正确找到数据文件。
"""

import os

# __file__ 指当前代码文件本身。取它所在目录再拼接子路径，
# 这样无论从哪个目录运行，都能定位到 data/scores.txt。
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "scores.txt")
REPORT_FILE = os.path.join(BASE_DIR, "output", "report.txt")


# ---------- 函数 1：读文件 ----------
def read_scores(filename):
    """读取成绩文件，返回 [[姓名, 分数], ...]，例如 [["张三", 85], ["李四", 92]]。

    文件每行一条记录，格式固定为「姓名,分数」。
    """
    students = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            # 按逗号切开：第 0 段是姓名，第 1 段是分数（转成整数）
            parts = line.strip().split(",")
            name = parts[0]
            score = int(parts[1])
            students.append([name, score])
    return students


# ---------- 函数 2：算平均分 ----------
def average(students):
    """计算平均分，返回浮点数。"""
    n = len(students)
    total = 0
    for stu in students:
        total = total + stu[1]
    return total / n


# ---------- 函数 3：找最高分 ----------
def max_score(students):
    """返回最高分。遍历一遍逐项比较，不修改传入的列表。"""
    m = students[0][1]
    for stu in students:
        if stu[1] > m:
            m = stu[1]
    return m


# ---------- 函数 4：数不及格人数 ----------
def count_failed(students):
    """返回分数低于 60 的人数。"""
    count = 0
    for stu in students:
        if stu[1] < 60:
            count = count + 1
    return count


# ---------- 函数 5：写报告文件 ----------
def write_report(filename, students, avg, mx, failed):
    """把统计结果写入文件。f.write() 只接受字符串，数字需先用 str() 转换。"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write("=====成绩收集=====\n")
        f.write("总人数：" + str(len(students)) + "\n")
        f.write("平均分：" + str(avg) + "\n")
        f.write("最高分：" + str(mx) + "\n")
        f.write("不及格人数：" + str(failed) + "\n")


# ---------- 主流程：把上面 5 个函数串起来 ----------
# __name__ == "__main__" 表示「只有直接运行本文件时才执行下面这些」。
# 因为 test_grade_tool.py 会 import 本文件，如果不加这个判断，
# 一旦被 import 就会把主流程跑一遍，还可能因为找不到文件直接报错。
if __name__ == "__main__":
    students = read_scores(DATA_FILE)
    print("读进来", len(students), "个学生")

    avg = average(students)
    mx = max_score(students)
    failed = count_failed(students)

    print("平均分：", avg)
    print("最高分：", mx)
    print("不及格人数：", failed)

    write_report(REPORT_FILE, students, avg, mx, failed)
    print("报告已写入", REPORT_FILE)
