# -*- coding: utf-8 -*-
"""
给 grade-tool 加一句大模型：把统计结果丢给 AMD 开发者平台（OpenAI 兼容接口），让它说人话。
这一个文件，就让简历上的项目从「脚本」升级成「LLM 应用」。

key 放在同目录的 key.txt（一行，只写 rc- 开头那串），已被 .gitignore 挡住，不会推到 GitHub。
换平台 / 换模型：只改下面「配置」三行。
"""
import os
import sys

import requests

from grade_tool import read_scores, average, max_score, count_failed, DATA_FILE

# ============ 配置（换平台只改这里）============
BASE_URL = "https://developer.amd.com.cn/radeon/v1"   # AMD 开发者平台（OpenAI 兼容）
# 依次尝试，前一个模型满负载(429)就自动换下一个
MODELS = ["DeepSeek-V4-Flash", "GLM-5.3-Flash", "Qwen3.8-27B"]
# ================================================

CHAT_URL = BASE_URL + "/chat/completions"              # 真正的对话接口地址
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_key():
    """先看环境变量，再看同目录 key.txt；都没有返回空。"""
    key = (os.environ.get("LLM_API_KEY", "") or os.environ.get("DEEPSEEK_API_KEY", "")).strip()
    if key:
        return key
    key_file = os.path.join(BASE_DIR, "key.txt")
    if os.path.exists(key_file):
        with open(key_file, "r", encoding="utf-8") as f:
            key = f.read().strip()
        # 真实 key 是一串不含空格/中文的英文数字（rc- 或 sk- 开头都行）
        if len(key) > 10 and key.isascii():
            return key
    return ""


def summarize(stats_text, api_key):
    """把统计数字 POST 给大模型，拿回一段人话点评。模型满负载会自动换下一个。"""
    headers = {
        "Authorization": "Bearer " + api_key,   # 身份令牌
        "Content-Type": "application/json",
    }
    messages = [
        {"role": "system", "content": "你是老师助理，用两三句中文点评成绩，语气客观，并给一句改进建议。"},
        {"role": "user", "content": "这是本次成绩统计：\n" + stats_text + "\n请生成一段 80 字以内的点评。"},
    ]

    for model in MODELS:
        payload = {"model": model, "messages": messages, "temperature": 0.7}
        resp = requests.post(CHAT_URL, json=payload, headers=headers, timeout=60)

        if resp.status_code == 401:
            print("key 无效或过期（401）。检查 key.txt 里的 key。")
            sys.exit(1)
        if resp.status_code == 200:
            # 字符串 -> 字典 -> 取内容（day11 的 loads 那一步）
            return resp.json()["choices"][0]["message"]["content"]

        print("%s 暂时不可用（%d），换下一个模型……" % (model, resp.status_code))

    print("模型都满了，稍等几分钟再跑。")
    sys.exit(1)


if __name__ == "__main__":
    key = load_key()
    if not key:
        print("没找到有效 key。把 key 放进 grade-tool/key.txt（一行，只写 key）。")
        sys.exit(1)

    students = read_scores(DATA_FILE)
    stats = "总人数 %d，平均分 %.1f，最高分 %d，不及格 %d 人。" % (
        len(students), average(students), max_score(students), count_failed(students)
    )
    print("统计结果：", stats)
    print("正在请大模型点评……")
    print("大模型点评：", summarize(stats, key))
