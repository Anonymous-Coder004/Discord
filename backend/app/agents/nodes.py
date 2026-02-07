# app/agents/nodes.py

from .state import LLMState
from .llm_connection import get_llm_model

model = get_llm_model()

async def llm_qa(state: LLMState) -> LLMState:
    prompt = f"Answer the following question: {state.ques}"

    result = await model.ainvoke(prompt)

    return LLMState(
        ques=state.ques,
        ans= result.content,
    )
