from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from models import TicketAction, TicketObs, TicketReward
from typing import Dict, Any

app = FastAPI(title="CyberTicket OpenEnv Backend")

# In-memory environment state
env_state = {
    "tickets": [],
    "system_load": 0.0,
    "last_action_status": "None",
    "step_count": 0,
    "cumulative_reward": 0.0
}

@app.get("/")
def read_root():
    """Redirect to the API documentation."""
    return RedirectResponse(url='/docs')

@app.post("/reset")
def reset_env(config: Dict[str, Any] = None):
    global env_state
    config = config or {}
    env_state = {
        "tickets": config.get("initial_tickets", []),
        "system_load": config.get("initial_load", 0.1),
        "last_action_status": "Environment reset.",
        "step_count": 0,
        "cumulative_reward": 0.0
    }
    return get_state()

@app.post("/step")
def step_env(action: TicketAction):
    global env_state
    reward_val = 0.0
    
    # Process the ticket action
    ticket = next((t for t in env_state["tickets"] if t["id"] == action.ticket_id), None)
    
    if not ticket:
        env_state["last_action_status"] = f"Error: Ticket {action.ticket_id} not found."
        env_state["system_load"] = min(1.0, env_state["system_load"] + 0.05)
    else:
        if action.action_type == "categorize":
            ticket["category"] = action.value
            env_state["last_action_status"] = f"Categorized {action.ticket_id} as {action.value}."
            # Reward: +0.2 for correct categorization (placeholder logic)
            if "Password" in action.value:
                reward_val += 0.2
                
        elif action.action_type == "escalate":
            if action.value == "Admin" and ticket.get("type") == "Server Down":
                env_state["last_action_status"] = f"Escalated {action.ticket_id} correctly to {action.value}."
                reward_val += 0.5 # Reward: +0.5 for correct priority
            else:
                env_state["last_action_status"] = f"Incorrect escalation for {action.ticket_id} to {action.value}."
                reward_val -= 0.2 # Penalty: -0.2 for incorrect escalation
                
        elif action.action_type == "close":
            env_state["tickets"] = [t for t in env_state["tickets"] if t["id"] != action.ticket_id]
            env_state["last_action_status"] = f"Closed ticket {action.ticket_id}."
            reward_val += 1.0 # Reward: +1.0 for task completion (close)
            
    env_state["step_count"] += 1
    env_state["cumulative_reward"] += reward_val
    
    # Slight increase in load over time, unless tickets are closed
    env_state["system_load"] = min(1.0, float(len(env_state["tickets"]) * 0.1))

    return {
        "obs": get_state().model_dump(),
        "reward": TicketReward(value=reward_val).model_dump(),
        "done": len(env_state["tickets"]) == 0
    }

@app.get("/state", response_model=TicketObs)
def get_state():
    return TicketObs(
        active_tickets=env_state["tickets"],
        system_load=env_state["system_load"],
        last_action_status=env_state["last_action_status"]
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
