from flask import Flask, render_template, request, jsonify
from ollama import Client
import os
import re
from datetime import datetime
from agent_code.ui_integrator import analysis

app = Flask(__name__)
app.secret_key = os.urandom(24)

def load_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def build_prompt(user_question, template, logs):
    return f"{user_question.strip()}\n\n" + template.replace("{LOG_CONTENT}", logs)

def analyze_logs(prompt):
    client = Client()
    response = client.chat(model="llama3", messages=[
        {"role": "user", "content": prompt}
    ])
    return response['message']['content']

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form['question'].strip()

    try:
        logs = load_file("app_logs.txt")

        # prompt_template = load_file("prompt_template.txt")
        # full_prompt = build_prompt(question, prompt_template, logs)

        analysis = analysis(question)


        # Convert markdown to HTML
        analysis = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', analysis)
        analysis = analysis.replace("\n", "<br>")

        with open("analysis_output.txt", "w", encoding='utf-8') as f:
            f.write(analysis)

        # Timestamp after analysis is complete
        timestamp = datetime.now().strftime('%I:%M %p')

        return jsonify({ "response": analysis, "timestamp": timestamp })

    except Exception as e:
        timestamp = datetime.now().strftime('%I:%M %p')
        return jsonify({ "response": f"❌ Error: {e}", "timestamp": timestamp })

if __name__ == '__main__':
    app.run(debug=True)
