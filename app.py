

from langchain.prompts import ChatPromptTemplate
from agent_code.agent.llm_handler import llm_json

def rephrase_input(question):
    # Step 1: Load chat history
    try:
        with open('agent_code/data/chat_memory_log.txt', "r", encoding="utf-8") as f:
            chat_history = f.read()
    except Exception as e:
        raise RuntimeError(f"Failed to read chat history: {e}")

    # Step 2: Define rephrasing prompt
    prompt_template_str = """You are a helpful AI assistant.

Using the following conversation history:
{chat_history}
Also focus on the last part of history since that have more context 
Also if quesry goes like is everyhting fine with all or with my system that means all the applications it is very very important
Rephrase the following question to make it fully self-contained and contextually complete:
Also if users ask for details then specifically mention very properly focusing on details 
Also if query doesn't have detail word or context then spefcifaclly include consise word in your response and the system i will pass your prompt doesnot have memory
{user_question}

Only return the rephrased question. Do not explain anything."""

    prompt = ChatPromptTemplate.from_template(prompt_template_str)

    # Step 3: Prepare and call LLM
    messages = prompt.format_messages(
        chat_history=chat_history,
        user_question=question
    )

    llm = llm_json()
    response = llm.invoke(messages)

    return response.content.strip()


# Then use it like:
# result = classify_query(rephrased)

from langchain.prompts import ChatPromptTemplate
from agent_code.agent.llm_handler import llm_json  # assuming this returns a LangChain-compatible chat model

def classify_query(input):
    question1 = input  # or question(rephrase_input) if that's a function

    llm = llm_json()

    template = '''You are a AI router for my project. My tools deal with three things only:
1. Summarize issues using logs
2. Create deployment architecture
3. Suggest fixes

I am providing you with a user query. You must return **true** or **false**, and **nothing else**, based on these rules:
Note : Very Very important if the query doesn't contain fixes or the immediate history doesnot contains fixes dont include suggest fixes or troubleshooting steps
- If the query asks for fixes → return **false**
- If the query includes both summaries and fixes → return **false**
- Otherwise → return **true**

Query:
{user_query}

Note: Do NOT return any explanation. Only return **true** or **false**. This is very important.'''

    # Create prompt
    prompt_template = ChatPromptTemplate.from_template(template)

    # Format the message
    messages = prompt_template.format_messages(user_query=question1)

    # Call the model
    response = llm.invoke(messages)

    # Clean output
    result = response.content.strip().lower()
    # print(result)

    # Return as boolean string (optional: validate output)
    if result not in {"true", "false"}:
        raise ValueError(f"Unexpected output: {result}")
    
    return result

from agent_code.agent.llm_handler import llm_json

from flask import Flask, render_template, request, jsonify
from ollama import Client
import os
import re
from datetime import datetime
from agent_code.ui_integrator import analysis
from flask import request, jsonify
from datetime import datetime
from datetime import datetime
# from agent_code.agent.rephraser_llm import rephrase_input
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
from app2 import task3
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/ask', methods=['POST'])
def ask():
    # print("POST /ask received")
    question = request.form['question'].strip()
    # print(question)

    try:
        # logs = load_file("app_logs.txt")
        # print(question)
        question1=rephrase_input(question)
        # llm=llm_json()
        # template= '''You are a AI router my project. My tools deal with three things only summarize issues using logs create deployment architecture 
        # and  last suggest fixes . I am providing you with user query what you need to do is return true of false it is very very importand return only true
        # or false based on the following conditions
        # 1 If query asks for fixes use return false
        # else return true
        # if query have both fixes and summaries then return false only

        # Note: You only have to return true or false nothing else this is very very very very important
        # '''
        # print(question)
        print(question1)
        a=classify_query(question1)
        print(a)


        print("******************************")
        if a == "true":  # ✅ compare string to string
            result = analysis(question1)
        else:
            result = task3(question1)
        with open('agent_code/data/chat_memory_log.txt', 'r') as f:
            hist=f.read()

        hist+=f'\nhuman:{question1}\nai: {result}'

        with open('agent_code/data/chat_memory_log.txt', 'w') as f:
            f.write(hist)


        with open("analysis_output.txt", "w", encoding='utf-8') as f:
            f.write(result)

        response_data = {"response": result}
        if "deployment diagram" in result.lower():
            response_data["image_url"] = "/static/final_output.png"

        return jsonify(response_data)

    except Exception as e:
        timestamp = datetime.now().strftime('%I:%M %p')
        return jsonify({ "response": f"❌ Error: {e}", "timestamp": timestamp })


if __name__ == '__main__':
    app.run(debug=True)


