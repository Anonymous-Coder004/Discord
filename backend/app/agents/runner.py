from .graph_builder import build_graph
from langchain_core.messages import AIMessage
graph = build_graph()

async def run_llm_from_messages(messages: list) -> str:
    result = await graph.ainvoke({"messages": messages})

    final_msg = result["messages"][-1]


    # If it's AIMessage object
    if isinstance(final_msg, AIMessage):
        content = final_msg.content

        # If content is list (tool-aware models sometimes return blocks)
        if isinstance(content, list):
            text_parts = []

            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text_parts.append(block.get("text", ""))

            return "".join(text_parts)

        return content

    # Fallback
    return str(final_msg)
