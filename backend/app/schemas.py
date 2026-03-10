from pydantic import BaseModel
from typing import Optional, List, Dict


class ChatRequest(BaseModel):
    model: str
    messages: List[Dict]
