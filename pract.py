# # # # # main.py
# # # # from agent_code.agent.react_agent import get_react_agent
# # # # from agent_code.agent.rephraser_llm import rephrase_input
# # # # def main():
# # # #     agent = get_react_agent()

# # # #     print("🤖 AI Agent is ready! Type your question (e.g., 'Summarize logs for App1') or type 'exit':\n")

# # # #     while True:
# # # #         query = input("User: ")
# # # #         if query.lower() in {"exit", "quit"}:
# # # #             break
# # # #         query = rephrase_input(agent.memory.chat_memory.messages, query)
# # # #         try:
# # # #             response = agent.invoke({"input": query})

# # # #             print(f"\nAgent: {response['output']}\n")

# # # #         except Exception as e:
# # # #             print(f"\n⚠️ Error: {e}\n")
# # # #     # query = "Is there anything wrong with App1?"
# # # #     # response = agent.invoke({"input": "Can you tell me the problems in the system?"})

# # # #     # print(response)



# # # # if __name__ == "__main__":
# # # #     main()
# # from agent_code.tools.tool3 import run_task1_log_summarization_tool

# # # Sample test input
# # app = "app1"
# # component = "comp1"
# # query = "Summarize the issues in app1 comp11"

# # # You must pass all required inputs as a dictionary to `.invoke()`
# # response = run_task1_log_summarization_tool.invoke({
# #     "app": app,
# #     "component": component,
# #     "query": query
# # })

# # print("=== Tool Output ===")
# # print(response)


# # # from agent_code.ui_integrator import analysis



# # # prompt='is everything fine with app1'
# # # print(analysis(prompt))


# # # from agent_code.agent.rephraser_llm import rephrase_input


# # # a=rephrase_input('', "please give details about what is wrong with the application1")

# # # # print(a)

# # from agent_code.ui_integrator import analysis


# # prompt='is everything fine with my app1'

# # result=analysis(prompt)
# # print(result)

# import os
# import json
# from agent_code.tools.tool2 import run_common_llm_tasks

# OUTPUT_PATH = "agent_code/data/out_put.json"

# def test_run_common_llm_tasks():
#     print("🔧 Running `run_common_llm_tasks()`...")
    
#     result = run_common_llm_tasks()
#     print("📦 Status:", result.status)
#     print("📝 Message:", result.message)

#     # Step 1: Check file existence
#     if not os.path.exists(OUTPUT_PATH):
#         print("❌ File `out_put.json` not found.")
#         return

#     # Step 2: Load the file
#     with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
#         try:
#             data = json.load(f)
#         except json.JSONDecodeError as e:
#             print("❌ JSON decode error:", str(e))
#             return

#     # Step 3: Validate contents
#     if not data:
#         print("⚠️ File exists but is empty.")
#     else:
#         print(f"✅ File contains {len(data)} log summary entries.")
#         print("🔍 Sample entry:", json.dumps(data[0], indent=2) if isinstance(data, list) else data)

# # Run the test
# if __name__ == "__main__":
#     test_run_common_llm_tasks()


# test_tool4.py

from agent_code.tools.tool4 import generate_deployment_diagram

def test_deployment_diagram_tool():
    print("🔧 Running deployment diagram tool...")

    result = generate_deployment_diagram.invoke({})

    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")
    print(f"Diagram Path: {result['data'] or 'N/A'}")

    if result['status'] == "success":
        print("🎉 Diagram generated successfully. You can open the PNG file at the given path.")
    else:
        print("❌ Test failed. Check the error message above.")

if __name__ == "__main__":
    test_deployment_diagram_tool()
