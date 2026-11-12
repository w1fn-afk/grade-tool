# -*- coding: utf-8 -*-
"""
成绩统计小工具
读 data/scores.txt -> 统计 -> 把结果写到 output/report.txt

只用 day1~day4 学的语法：变量、列表、函数、for、if、字符串处理、文件读写
没有第三方库，没有类，没有花哨语法。
"""

import os
from re import M

# __file__ 就是"这个代码文件自己"，取它所在的文件夹，再拼上子路径。
# 这样不管你在哪个文件夹运行，都能找到 data/scores.txt，不会报"找不到文件"。
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "scores.txt")
REPORT_FILE = os.path.join(BASE_DIR, "output", "report.txt")


# ---------- 函数 1：读文件 ----------
def read_scores(filename):
    """读成绩文件，返回 [[名字, 分数], ...]，比如 [["张三", 85], ["李四", 92]]"""
    # TODO 1（参考你 day4 做过的 quiz5）
    # 1. 建一个空列表 students
    students=[]
    # 2. 用 with open(filename, "r", encoding="utf-8") as f:
    with open(filename,"r",encoding="utf-8") as f:
    # 3.     用 for line in f: 一行一行读
        for line in f:
    # 4.     parts = line.strip().split(",")   # 按逗号切开
            parts = line.strip().split(",")
    # 5.     name = parts[0]                    # 第 0 段是名字
            name = parts[0]
    # 6.     score = int(parts[1])              # 第 1 段是分数，转成数字
            score = int(parts[1])
    # 7.     students.append([name, score])     # append = 往列表末尾加一项
            students.append([name, score])
    # 8. 最后 return students
    return students


# ---------- 函数 2：算平均分 ----------
def average(students):
    """算所有人的平均分，返回一个数字（可能是小数）"""
    # TODO 2：把所有人的分数加起来，再除以人数。
    # 自己想：分数藏在 students 每一项的哪个位置？人数怎么得到？
    s = len(students)
    total = 0
    for stu in students:
        total = total + stu[1]
    return total/s
    
        



# ---------- 函数 3：找最高分 ----------
def max_score(students):
    """返回最高分（就是你刚想通的"打擂台"）"""
    # TODO 3：打擂台找最高分，只记录、不动列表。
    m = students[0][1]
    for stu in students:
        if  stu[1]> m:
            m = stu[1]
    return m


# ---------- 函数 4：数不及格人数 ----------
def count_failed(students):
    """返回分数 < 60 的人数"""
    # TODO 4：数一数有几个分数低于 60。
    # 自己想：用一个变量记账，满足了就加一，这叫什么套路？（你写过很多次了）
    count = 0
    for stu in students:
        if stu[1] < 60:
            count = count + 1
    return count

# ---------- 函数 5：写报告文件 ----------
def write_report(filename, students, avg, mx, failed):
    """把统计结果写到文件里"""
    # TODO 5：用 day4 学的方式打开一个文件（写模式），把统计结果写进去。
    # 自己想：f.write() 只能写文字，avg 和 mx 是数字，怎么办？（提示：str()）
    # 至少写：标题 + 总人数 + 平均分 + 最高分 + 不及格人数，每行一个。
    with open(filename,"w",encoding="utf-8") as f:
        f.write("=====成绩收集=====\n")
        f.write("总人数："+ str(len(students))+ "\n")
        f.write("平均分："+ str(avg)+ "\n")
        f.write("最高分："+ str(mx) + "\n")
        f.write("不及格人数："+ str(failed)+ "\n")
        
    


# ---------- 主流程：把上面 5 个函数串起来 ----------
# 这部分我已经写好了，你先读懂它：先读文件，再算，最后写报告
#
# 注意这个 if：意思是"只有直接运行本文件时，下面代码才执行"。
# 因为测试文件会 import 本文件，如果不加这个判断，
# 测试一 import 就会把主流程跑一遍，还可能因为找不到文件直接报错。
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
