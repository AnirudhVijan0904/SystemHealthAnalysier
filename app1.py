from flask import Flask, render_template, request, jsonify
from ollama import Client
import os
import re
from datetime import datetime
from agent_code.ui_integrator import analysis
from flask import request, jsonify
from datetime import datetime
from datetime import datetime
def get_time():
    now = datetime.now()
    hours = now.hour % 12 or 12
    minutes = str(now.minute).zfill(2)
    am_pm = 'AM' if now.hour < 12 else 'PM'
    return f"{hours}:{minutes} {am_pm}"


app = Flask(__name__)
app.secret_key = os.urandom(24)

# def load_file(path):
#     with open(path, 'r', encoding='utf-8') as f:
#         return f.read()

# def build_prompt(user_question, template, logs):
#     return f"{user_question.strip()}\n\n" + template.replace("{LOG_CONTENT}", logs)

# def analyze_logs(prompt):
#     client = Client()
#     response = client.chat(model="llama3", messages=[
#         {"role": "user", "content": prompt}
#     ])
#     return response['message']['content']

@app.route('/')
def index():
    return render_template("index1.html")

@app.route('/ask', methods=['POST'])
def ask():
    # print("POST /ask received")
    question = request.form['question'].strip()
    # print(question)

    try:
        # logs = load_file("app_logs.txt")
        # print(question)
        result=analysis(question)

        with open("analysis_output.txt", "w", encoding='utf-8') as f:
            f.write(result)

        # Timestamp after analysis is complete
        # timestamp = datetime.now().strftime('%I:%M %p')

        return jsonify({ "response": result })

    except Exception as e:
        timestamp = datetime.now().strftime('%I:%M %p')
        return jsonify({ "response": f"❌ Error: {e}", "timestamp": timestamp })


if __name__ == '__main__':
    app.run(debug=True)
