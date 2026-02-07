# app/agents/graph_builder.py

from langgraph.graph import StateGraph, START, END
from .state import LLMState
from .nodes import llm_qa

def build_graph():
    graph = StateGraph(LLMState)

    graph.add_node("llm_qa", llm_qa)
    graph.add_edge(START, "llm_qa")
    graph.add_edge("llm_qa", END)

    return graph.compile()
