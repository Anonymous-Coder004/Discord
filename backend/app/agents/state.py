from pydantic import BaseModel
from typing import List, Dict, Any


class ChatState(BaseModel):
    messages: List[Dict[str, Any]]
