from pydantic import BaseModel
from typing import List, Literal, Dict, Any, Optional

class TicketAction(BaseModel):
    ticket_id: str
    action_type: str
    value: str
    task_id: Optional[str] = None
