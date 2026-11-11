from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage


class State(TypedDict):
    messages: Annotated[list,add_messages]

def chatbot(state:State):
    return {"messages":[AIMessage(content="Hello this is a message from chatbot")]}

def sample(state:State):
    return {

      "messages":[AIMessage(content="Hello this a message from sample node")]  
    }        


builder = StateGraph(State)
builder.add_node("chatbot",chatbot)
builder.add_node("sample",sample)

builder.add_edge(START,"chatbot")
builder.add_edge("chatbot","sample")
builder.add_edge("sample",END)

graph = builder.compile()

updated_state = graph.invoke(
   {"messages": [{"role": "user", "content": "Hi, my name is Harsh"}]}
)

print(updated_state)