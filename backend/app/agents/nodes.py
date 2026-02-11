from .llm_connection import get_llm_model
from .state import ChatState
from langgraph.prebuilt import ToolNode
from .tools import get_tools


async def chat_node(state: ChatState):
    messages = state["messages"]

    # Lazy load model + tools
    model = get_llm_model()
    tools = get_tools()

    model_tools = model.bind_tools(tools)

    response = await model_tools.ainvoke(messages)

    return {
        "messages": [response]
    }


def get_tool_node():
    return ToolNode(get_tools())
