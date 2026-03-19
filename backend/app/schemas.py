from typing import Dict, List, Optional

from pydantic import BaseModel


class ChatRequest(BaseModel):
    model: str
    messages: List[Dict]
