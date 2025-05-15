#!/usr/bin/env python3
import os
import sys
import json
from openai import OpenAI

# 设置缓存路径
HISTORY_FILE = os.path.expanduser("./qwen_history.json")

# 获取 API Key
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 获取用户输入
if len(sys.argv) < 2:
    print("用法: qwen '你的问题' 或 qwen clear")
    sys.exit(1)

user_input = " ".join(sys.argv[1:])

# 清空历史指令
if user_input.lower() in ["clear", "--clear", "-c"]:
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
        print("✅ 上下文已清除")
    else:
        print("⚠️ 没有历史记录")
    sys.exit(0)

# 加载历史上下文
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        messages = json.load(f)
else:
    messages = [{'role': 'system', 'content': 'You are a helpful assistant.'}]

# 添加新问题
messages.append({'role': 'user', 'content': user_input})

# 请求大模型
response = client.chat.completions.create(
    model="qwen-plus",
    messages=messages
)

reply = response.choices[0].message.content.strip()
print(reply)

# 添加回复到历史
messages.append({'role': 'assistant', 'content': reply})

# 保存历史上下文
with open(HISTORY_FILE, "w", encoding="utf-8") as f:
    json.dump(messages, f, indent=2, ensure_ascii=False)
