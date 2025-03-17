
import os
import requests
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Set your OpenRouter API key
API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# In-memory task storage for the daily planner
daily_tasks = []

def get_chatbot_response(user_message):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "openai/gpt-3.5-turbo",  # You can use "openai/gpt-3.5-turbo"
        "messages": [{"role": "user", "content": user_message}],
        "max_tokens": 150
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response_json = response.json()
        return response_json["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/")
def index():
    return render_template("index.html", tasks=daily_tasks)

@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.form["message"]
    
    # If user wants to add to the daily planner
    if user_message.lower().startswith("add task"):
        task = user_message[len("add task"):].strip()  # Extract the task
        daily_tasks.append(task)
        return jsonify({"user": user_message, "bot": "Task added to your daily planner!"})
    
    # If user wants to view the daily planner
    if user_message.lower() == "show tasks":
        tasks = "\n".join(daily_tasks) if daily_tasks else "No tasks for today."
        return jsonify({"user": user_message, "bot": f"Your tasks: {tasks}"})
    
    # Regular chatbot interaction
    bot_response = get_chatbot_response(user_message)
    return jsonify({"user": user_message, "bot": bot_response})

if __name__ == "__main__":
    app.run(debug=True)

