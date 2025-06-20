# main.py
from agent.react_agent import get_react_agent
from agent.rephraser_llm import rephrase_input
def main():
    agent = get_react_agent()

    print("🤖 AI Agent is ready! Type your question (e.g., 'Summarize logs for App1') or type 'exit':\n")

    while True:
        query = input("User: ")
        if query.lower() in {"exit", "quit"}:
            break
        query = rephrase_input(agent.memory.chat_memory.messages, query)
        try:
            response = agent.invoke({"input": query})

            print(f"\nAgent: {response['output']}\n")

        except Exception as e:
            print(f"\n⚠️ Error: {e}\n")
    # query = "Is there anything wrong with App1?"
    # response = agent.invoke({"input": "Can you tell me the problems in the system?"})

    # print(response)



if __name__ == "__main__":
    main()

