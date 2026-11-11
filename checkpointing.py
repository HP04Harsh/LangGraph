import os
from typing import Annotated
from typing_extensions import TypedDict
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.mongodb import MongoDBSaver

load_dotenv()


class State(TypedDict):
    messages: Annotated[list, add_messages]

llm = init_chat_model(
    "qwen/qwen3.8-27b",
    model_provider="groq",
    api_key=os.getenv("GROQ_API"),
)

def chatgpt(state:State):
    return {"messages": [llm.invoke(state["messages"])]}

builder = StateGraph(State)
builder.add_node("chatgpt", chatgpt)
builder.add_edge(START, "chatgpt")
builder.add_edge("chatgpt", END)

with MongoDBSaver.from_conn_string("mongodb://localhost:27017") as saver:
    graph = builder.compile(checkpointer=saver)
    config =  {"configurable": {"thread_id": "harsh"}}
    r1 = graph.invoke(
        {"messages": [{"role": "user", "content": "Hi, My name is Harsh Pardhi"}]},
        config=config,
    )
    print("AI:", r1["messages"][-1].content)

    r2 = graph.invoke(
        {
            "messages":[{"role":"user","content":"Hi, What is my name?"}]
        },
        config=config,
    ) 

    print("AI:",r2["messages"][-1].content)


    snapshot = graph.get_state(config)
    print("Total saved messages:", len(snapshot.values["messages"]))