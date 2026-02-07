from .graph_builder import build_graph
from .state import LLMState

graph = build_graph()


async def run_llm(user_input: str) -> str:
    initial_state = LLMState(ques=user_input)

    result = await graph.ainvoke(initial_state)

    # LangGraph returns dict → convert back to model
    final_state = LLMState(**result)

    return final_state.ans
