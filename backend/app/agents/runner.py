from .graph_builder import build_graph

graph = build_graph()


async def run_llm_from_messages(messages: list) -> str:
    result = await graph.ainvoke({
        "messages": messages
    })

    return result["messages"][-1]["content"]
