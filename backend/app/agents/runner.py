from .graph_builder import build_graph
from langchain_core.messages import AIMessage

_graph = None


def get_graph():
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph


async def run_llm_from_messages(messages: list) -> str:
    graph = get_graph()

    result = await graph.ainvoke({"messages": messages})

    final_msg = result["messages"][-1]

    if isinstance(final_msg, AIMessage):
        content = final_msg.content

        if isinstance(content, list):
            text_parts = []

            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text_parts.append(block.get("text", ""))

            return "".join(text_parts)

        return content

    return str(final_msg)
