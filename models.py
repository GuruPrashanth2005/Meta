from pydantic import BaseModel, Field
from typing import List, Literal, Dict, Any

class TicketAction(BaseModel):
    ticket_id: str = Field(..., description="ID of the ticket to action on")
    action_type: Literal["categorize", "escalate", "close"] = Field(..., description="Action to take")
    value: str = Field(..., description="Value for the action (e.g., category name, user to assign, or close reason)")

class TicketObs(BaseModel):
    active_tickets: List[Dict[str, Any]] = Field(..., description="Current list of active tickets")
    system_load: float = Field(..., description="Current system load (0.0 to 1.0)")
    last_action_status: str = Field(..., description="Status of the last action taken")

class TicketReward(BaseModel):
    value: float = Field(..., description="Reward value for the step")
