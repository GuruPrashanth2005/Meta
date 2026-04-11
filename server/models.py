from pydantic import BaseModel
from typing import List, Literal, Dict, Any, Optional

class TicketAction(BaseModel):
    ticket_id: str
    action_type: Literal["categorize", "set_priority", "close_ticket"]
    value: str
    task_id: Optional[str] = None

class TicketObs(BaseModel):
    active_tickets: List[Dict[str, Any]]
    system_load: float
    last_action_status: str

class TicketReward(BaseModel):
    value: float
