# 成绩统计小工具

一个用 Python 写的成绩统计小项目，按三个版本迭代：

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

## 设计取舍

**为什么用 SQLite 而不是 MySQL / PostgreSQL**
这个工具的定位是本地单人使用、无需部署。SQLite 是 Python 内置模块，零安装、单文件，
备份就是复制一个 `.db` 文件。换成服务型数据库不会带来任何收益，只会增加部署和运维负担。

**为什么只引入 `requests` 一个第三方库**
v1 和 v2 只用 `os` / `sqlite3` 这类标准库，小工具不值得为一点功能引入依赖链。
v3 需要做 HTTP 请求和 JSON 编解码，手写 `urllib` 反而增加出错面，因此只引入 `requests`。

**为什么 key 不写在代码里**
key 写在代码里，一次提交就会永久留在 git 历史中，即使后续删除也仍可被检出。
因此 key 从环境变量读取，本地调试时回退到 `key.txt`，并由 `.gitignore` 拦截。

**为什么要有模型降级**
免费额度的模型在高峰期会返回 429（并发超限）。单模型调用一旦失败整个流程就中断，
因此按列表顺序依次尝试，前一个不可用自动切换到下一个，提高流程的可用性。

## 已知局限与后续方向

- 输入文件格式固定为「姓名,分数」，遇到空行或字段缺失会抛异常，尚未做容错
- 数据库路径写死为 `data/scores.db`，不支持命令行参数指定，可用 `argparse` 改进
- 没有并发控制，多个进程同时写入可能冲突
- 统计结果目前只输出文本报告，可扩展导出 CSV / Excel
