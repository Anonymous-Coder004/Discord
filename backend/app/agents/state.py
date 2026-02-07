# app/agents/state.py

from pydantic import BaseModel


class LLMState(BaseModel):
    ques: str
    ans: str = ""
