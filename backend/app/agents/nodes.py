from .llm_connection import get_llm_model
from .state import ChatState
from langgraph.prebuilt import ToolNode
from .tools import tools

model = get_llm_model()
model_tools = model.bind_tools(tools)


async def chat_node(state: ChatState):
    # Access dict-style
    messages = state["messages"]

    response = await model_tools.ainvoke(messages)

    # DO NOT manually append previous messages
    # add_messages reducer handles that automatically
    return {
        "messages": [response]
    }


tool_node = ToolNode(tools)
