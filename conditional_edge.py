from typing import Literal, Optional
from typing_extensions import TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.mongodb import MongoDBSaver 
import groq
import os

load_dotenv()
client = groq.Client(api_key=os.getenv('GROQ_API'))

class State(TypedDict):
    user_query: str
    llm_output: Optional[str]    
    is_good: Optional[bool]


def ask(model:str, query:str)->str:
    response = client.chat.completions.create(
        model = model,
        messages = [
            {"role":"user","content":query}
        ]
    )
    return response.choices[0].message.content


def qwen(state:State):
    print("-----Using Qwen-----")
    return {"llm_output": ask("qwen/qwen3.8-27b",state["user_query"])}

def chatgpt(state:State):
    print("-----Using ChatGPT------")
    return { "llm_output": ask("openai/gpt-oss-120b",state["user_query"])}    

def end_node(state: State):
    print("End node")
    return state

def evaluate_response(state: State) -> Literal["chatgpt", "end_node"]:
    print("Evaluate node — decision ho raha hai...")
    if state.get("is_good"):
        return "end_node"          
    return "chatgpt"    




builder = StateGraph(State)
builder.add_node("qwen", qwen)
builder.add_node("chatgpt", chatgpt)
builder.add_node("end_node", end_node)

builder.add_edge(START, "qwen")
builder.add_conditional_edges("qwen", evaluate_response) 
builder.add_edge("chatgpt", "end_node")
builder.add_edge("end_node", END)

graph = builder.compile()
print(graph.invoke({"user_query": "what is your name", "is_good": False}))        