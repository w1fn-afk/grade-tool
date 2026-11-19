# 成绩统计小工具

一个用 Python 写的完整小项目，经历了三代演进：

1. **v1（txt 版）**：读 `data/scores.txt` → 算平均分/最高分/不及格 → 写报告
2. **v2（SQLite 版）**：数据存进 SQLite 数据库，用 SQL 查询、分组、排序
3. **v3（LLM 版）**：把统计结果发给大模型，自动生成中文分析摘要

尽量只用 Python 自带标准库（v3 发 HTTP 请求用到 `requests`）。

## 各版本能干什么

### v1 · `grade_tool.py`（txt 版）
- 从 `data/scores.txt` 读取学生姓名和分数（每行一个，逗号隔开）
- 算出平均分、最高分、不及格人数
- 终端打印摘要，并把完整报告写到 `output/report.txt`

### v2 · `grade_tool_sqlite.py`（SQLite 版）
- 把成绩存进 `data/scores.db`（SQLite，Python 自带，零安装）
- 用 SQL 演示六个关键字：`SELECT / WHERE / GROUP BY / JOIN / ORDER BY / LIMIT`
- 额外统计及格率（及格人数 ÷ 总人数）

### v3 · `llm_summary.py`（LLM 版）
- 读取统计结果，POST 给 OpenAI 兼容接口（本项目用 AMD 开发者平台）
- 大模型返回一段中文点评，自动生成「人话分析」
- key 与代码分离（本地 `key.txt` + `.gitignore` 保护）
- 多模型自动降级：一个满负载（429）自动换下一个

## 项目结构

```
grade-tool/
├── grade_tool.py          # v1 主程序（txt → 统计 → 报告）
├── grade_tool_sqlite.py   # v2 SQLite 版（建表/查询/分组/JOIN/排序/及格率）
├── llm_summary.py         # v3 LLM 版（调大模型生成分析摘要）
├── test_grade_tool.py     # v1 验收脚本
├── key.txt                # 本地 key（被 .gitignore 忽略，不上传）
├── data/
│   └── scores.txt         # v1 输入数据
└── output/
    └── .gitkeep
```

## 怎么运行

```bash
# v1：txt 版
python grade_tool.py

# v2：SQLite 版
python grade_tool_sqlite.py

# v3：LLM 版（需先在 key.txt 填入 API key）
python llm_summary.py
```

跑 v1 的验收脚本：

```bash
python test_grade_tool.py
```

## 安全说明：key 不上仓库

`llm_summary.py` 需要的 API key 放在本地 `key.txt`；`.gitignore` 已忽略 `key.txt`、`*.key`、`scores.db`，**不会推到 GitHub**。程序会先读环境变量，没有再读 `key.txt`。

## 简历上怎么写

> **成绩统计工具**（Python，独立开发，含 SQLite + LLM 集成）
> - 使用 Python 标准库实现成绩数据的批量读取、统计与报告生成；
> - 升级为 SQLite 存储，用 SQL 完成条件查询、分组统计（GROUP BY）、多表关联（JOIN）与排序，并统计及格率；
> - 对接 OpenAI 兼容大模型接口，将统计结果自动生成中文分析摘要，实现「数据 → 结论」的自动化；
> - key 与代码分离并纳入 .gitignore 保护，实现多模型降级重试，保证调用稳定性。

## 继续升级的方向

- 异常处理：处理文件不存在、分数不是数字、接口超时等情况
- 用 `argparse` 让文件名可以从命令行传入
- 把统计结果同时导出成 CSV / Excel
