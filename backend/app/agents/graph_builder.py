from langgraph.graph import StateGraph, START, END
from .state import ChatState
from .nodes import chat_node,get_tool_node
from langgraph.prebuilt import tools_condition

def build_graph():
    builder = StateGraph(ChatState)

    builder.add_node("chat", chat_node)
    builder.add_node("tools", get_tool_node())
    builder.add_edge(START, "chat")
    builder.add_conditional_edges("chat", tools_condition) 
    builder.add_edge("tools", "chat")     
    return builder.compile()
