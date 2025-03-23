from flask import Flask, request, jsonify
from google import genai
import os

app = Flask(__name__)

# 初始化生成内容的客户端（请确保 API Key 安全存储，不要硬编码到代码中）
client = genai.Client(api_key=os.getenv("API_KEY"))

def generate_reply(conversation_history, user_input):
    prompt = (
        f"Below is the conversation history:\n{conversation_history}\n"
        f"The user just said: {user_input}\n"
        "Please generate a coherent and appropriate reply based on the above context:"
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    reply = response.text.strip()
    return reply

def summarize_conversation(conversation_history):
    prompt = (
        f"Please provide a concise summary of the following conversation:\n{conversation_history}\n"
        "Summary:"
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    summary = response.text.strip()
    return summary

@app.route("/api/chat", methods=["POST"])
def chat():
    # 获取 JSON 数据
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON payload"}), 400

    # 从前端传来的数据中获取用户消息与对话历史
    user_input = data.get("message")
    conversation_history = data.get("conversation", "")

    if not user_input:
        return jsonify({"error": "Missing user message"}), 400

    # 调用对话逻辑，生成回复
    reply = generate_reply(conversation_history, user_input)

    # 返回 JSON 格式的回复
    return jsonify({"reply": reply})

@app.route("/api/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    conversation_history = data.get("conversation", "")
    if not conversation_history:
        return jsonify({"error": "Missing conversation history"}), 400

    summary = summarize_conversation(conversation_history)
    return jsonify({"summary": summary})

if __name__ == "__main__":
    app.run(debug=True)

