from .llm_connection import get_llm_model
from .state import ChatState
model = get_llm_model()


async def chat_node(state: ChatState):
    response = await model.ainvoke(state.messages)
 
    return {
        "messages": state.messages + [
            {
                "role": "assistant",
                "content": response.content,
            }
        ]
    }
