from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class PersonaModel(BaseModel):
    id: str
    name: str
    belief: str
    tone: str
    background: str
    system_prompt: str

class DialogueRequest(BaseModel):
    topic: str
    persona1_id: str
    persona2_id: str
    turns: int = 3

class MessageModel(BaseModel):
    speaker: str
    message: str

class DialogueResponse(BaseModel):
    conversation: List[MessageModel]

class WebSocketRequest(BaseModel):
    topic: str
    persona1_id: str
    persona2_id: str
    turns: Optional[int] = 3