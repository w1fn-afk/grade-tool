# -*- coding: utf-8 -*-
"""
grade-tool 升级版：把数据从 txt 换成 SQLite 数据库

为什么要升级？
- 简历上「数据库」这一栏现在还是空的，SQL 是算法/应用岗的隐性门槛。
- 这个文件只用 Python 自带的标准库 sqlite3（不用 pip 装任何东西），
  把上一版 grade_tool 的「读 txt -> 统计」升级成「查数据库 -> 统计」。

SQL 面试只考六个关键字，本文件把它们全用一遍：
  SELECT    查什么
  WHERE     按条件筛
  GROUP BY  分组统计
  JOIN      拼表
  ORDER BY  排序
  LIMIT     只要前几条

先跑起来看输出，再逐段读注释。
"""
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "data", "scores.db")


# ---------- 第 0 步：连数据库（相当于打开文件） ----------
def connect():
    """打开 scores.db，没有就新建。返回 conn（连接对象）。"""
    return sqlite3.connect(DB_FILE)


# ---------- 第 1 步：建表 ----------
def create_tables(conn):
    """建两张表：students（学生成绩）+ classes（班级信息）。

    表 = 一张二维表格，每一行是一条记录，每一列是一个字段。
    """
    cur = conn.cursor()  # cursor = 游标，帮你执行 SQL 的"手"

    # students 表：4 个字段
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,  -- 自增编号
            name     TEXT,                               -- 姓名
            score    INTEGER,                            -- 分数
            class_id INTEGER                             -- 班级编号
        )
    """)

    # classes 表：班级编号 -> 班名 + 班主任（专门用来演示 JOIN）
    cur.execute("""
        CREATE TABLE IF NOT EXISTS classes (
            class_id   INTEGER PRIMARY KEY,
            class_name TEXT,
            teacher    TEXT
        )
    """)
    conn.commit()  # 提交 = 保存（写文件要 close，写数据库要 commit）


# ---------- 第 2 步：放数据 ----------
def seed_data(conn):
    """塞进 12 个学生（3 个班 x 4 人）+ 3 个班的信息。"""
    cur = conn.cursor()

    # 如果表里已经有数据就跳过，避免重复插入
    cur.execute("SELECT COUNT(*) FROM students")
    if cur.fetchone()[0] > 0:
        return

    students = [
        # (姓名, 分数, 班级编号)
        ("张三", 85, 1), ("李四", 92, 1), ("王五", 58, 1), ("赵六", 76, 1),
        ("钱七", 43, 2), ("孙八", 90, 2), ("周九", 67, 2), ("吴十", 55, 2),
        ("郑十一", 88, 3), ("冯十二", 72, 3), ("陈十三", 95, 3), ("林十四", 49, 3),
    ]
    cur.executemany(
        "INSERT INTO students (name, score, class_id) VALUES (?, ?, ?)",
        students,
    )

    classes = [
        (1, "一班", "王老师"),
        (2, "二班", "李老师"),
        (3, "三班", "张老师"),
    ]
    cur.executemany(
        "INSERT INTO classes (class_id, class_name, teacher) VALUES (?, ?, ?)",
        classes,
    )
    conn.commit()


# ---------- 第 3 步：六个关键字，逐个演示 ----------

def demo_select(conn):
    """SELECT：查出所有学生。* 表示"所有字段"。"""
    cur = conn.cursor()
    cur.execute("SELECT name, score FROM students")
    print("【SELECT】全部学生：", cur.fetchall())


def demo_where(conn):
    """WHERE：筛出不及格（score < 60）的人。"""
    cur = conn.cursor()
    cur.execute("SELECT name, score FROM students WHERE score < 60")
    print("【WHERE】不及格：", cur.fetchall())


def demo_groupby(conn):
    """GROUP BY：按班级分组统计。这是简历上「按班级分组统计」的核心。"""
    cur = conn.cursor()
    cur.execute("""
        SELECT class_id, COUNT(*), AVG(score), MAX(score)
        FROM students
        GROUP BY class_id
    """)
    print("【GROUP BY】每班 [人数, 平均分, 最高分]：")
    for row in cur.fetchall():
        print("   班级%d：人数 %d，平均 %.1f，最高 %d" % (row[0], row[1], row[2], row[3]))


def demo_join(conn):
    """JOIN：把 students 和 classes 拼起来，看班名和班主任。"""
    cur = conn.cursor()
    cur.execute("""
        SELECT s.name, s.score, c.class_name, c.teacher
        FROM students s
        JOIN classes c ON s.class_id = c.class_id
    """)
    print("【JOIN】学生 + 班名 + 班主任（前 3 条）：", cur.fetchall()[:3])


def demo_orderby_limit(conn):
    """ORDER BY + LIMIT：按平均分从高到低，只取前 2 名的班级。"""
    cur = conn.cursor()
    cur.execute("""
        SELECT c.class_name, AVG(s.score) AS avg_score
        FROM students s
        JOIN classes c ON s.class_id = c.class_id
        GROUP BY c.class_name
        ORDER BY avg_score DESC
        LIMIT 2
    """)
    print("【ORDER BY + LIMIT】平均分前 2 名的班：", cur.fetchall())

def demo_pass_rate(conn):
    """算及格率：及格人数 / 总人数"""
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM students WHERE score >= 60") 
    passed = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM students")
    total = cur.fetchone()[0]

    rate =passed/total
    print("【及格率】%d / %d = %.1f%%" % (passed, total, rate * 100))



if __name__ == "__main__":
    conn = connect()
    create_tables(conn)
    seed_data(conn)
    demo_select(conn)
    demo_where(conn)
    demo_groupby(conn)
    demo_join(conn)
    demo_orderby_limit(conn)
    demo_pass_rate(conn)
    conn.close()
    print("数据库文件在：", DB_FILE)
