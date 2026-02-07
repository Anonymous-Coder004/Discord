# test_llm.py

from app.services.llm_service import handle_llm_request

result = handle_llm_request(
    room_id=1,
    user_id=1,
    text="Explain LangGraph in simple terms."
)

print(result)
