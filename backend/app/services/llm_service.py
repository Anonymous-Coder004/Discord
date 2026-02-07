# app/services/llm_service.py

from app.agents.runner import run_llm


async def handle_llm_request(
    *,
    room_id: int,
    user_id: int,
    text: str,
) -> str:
    """
    Orchestrates LLM call.
    No WebSocket logic.
    No DB logic.
    Just returns AI response.
    """

    # Later:
    # - Add permission checks
    # - Add RAG routing
    # - Add memory
    # - Add rate limiting

    response = await run_llm(text)

    return response
