# 成绩统计小工具

用 Python 写的第一个完整小项目：读成绩文件 → 算统计 → 把结果写回文件。

只用 Python 自带的标准库，**没有第三方依赖**，全程只用变量、列表、函数、for、if、字符串处理、文件读写这些基础语法。

## 它能干什么

- 从 `data/scores.txt` 读取学生的姓名和分数（每行一个，逗号隔开）
- 自动算出 **平均分、最高分、不及格人数**
- 在终端打印摘要，同时把完整报告写到 `output/report.txt`

## 项目结构

```
grade-tool/
├── grade_tool.py          # 主程序（5 个函数 + 主流程）
├── test_grade_tool.py     # 验收脚本
├── data/
│   └── scores.txt         # 输入数据（10 条示例）
├── output/
│   └── .gitkeep           # 占位文件，保证 Git 跟踪这个文件夹
└── README.md              # 本文件
```

## 怎么运行

在项目文件夹里打开终端：

```bash
python grade_tool.py
```

跑验收测试：

```bash
python test_grade_tool.py
```

全部显示 `[通过]`，就说明做完了。

## 简历上怎么写

> **成绩统计工具**（Python，独立开发）
> - 使用 Python 标准库实现文本成绩数据的批量读取与解析，支持结构化提取姓名与分数；
> - 封装平均分、最高分、不及格人数等统计函数，对 10 条样本数据完成自动化计算；
> - 实现统计报告的本地持久化输出，将结果格式化写入文件；
> - 编写验收脚本覆盖核心函数与边界情况（如全负数场景），保证计算正确。

四行分别对应：**数据读取 → 核心算法 → 结果输出 → 测试**。面试时你要能讲清每一行代码为什么这么写。

## 怎么挂到 GitHub（Windows 详细步骤）

1. 注册并登录 [GitHub](https://github.com)
2. 下载安装 [Git](https://git-scm.com/download/win)（一路默认安装即可）
3. 在 GitHub 网页右上角点 **+** → **New repository**
   - Repository name 填 `grade-tool`
   - 其他保持默认，点 **Create repository**
4. 在项目文件夹里打开终端（或 Git Bash），依次敲这四行：

```bash
git init
git add .
git commit -m "第一个 Python 小项目：成绩统计工具"
git branch -M main
```

5. 再去 GitHub 仓库页面复制那串地址（形如 `https://github.com/你的用户名/grade-tool.git`），继续敲：

```bash
git remote add origin 你的仓库地址
git push -u origin main
```

6. 刷新 GitHub 页面，代码就上去了。

## 怎么继续升级这个项目

等你学了 day5 之后，可以回来加这些功能，让简历项目更厚：

- 学**列表推导式**后：把"取所有分数"的循环压缩成一行
- 学**异常处理**后：处理"文件不存在""分数不是数字"这些情况
- 学 **CSV** 后：把数据从 txt 换成 csv 格式
- 学**命令行参数**后：让文件名可以从命令行传入，而不是写死在代码里
