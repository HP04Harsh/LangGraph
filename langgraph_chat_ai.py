import os
from typing import Annotated
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

load_dotenv()


class State(TypedDict):
    messages: Annotated[list, add_messages]


llm = init_chat_model(
    "qwen/qwen3.8-27b",
    model_provider="groq",
    api_key=os.getenv("GROQ_API"),
)


def chatbot(state: State):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


builder = StateGraph(State)
builder.add_node("chatbot", chatbot)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)
graph = builder.compile()

messages = []
print("Chat started. Type 'exit' or 'quit' to end.")

while True:
    try:
        user_input = input("You: ").strip()
    except EOFError:
        break

    if user_input.lower() in {"exit", "quit"}:
        break
    if not user_input:
        continue

    result = graph.invoke({"messages": messages + [{"role": "user", "content": user_input}]})
    messages = result["messages"]
    print(f"Assistant: {messages[-1].content}")
