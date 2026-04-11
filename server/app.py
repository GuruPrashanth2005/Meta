from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from server.models import TicketAction, TicketObs, TicketReward
from typing import Dict, Any
from server.tasks import TASK_GRADERS
import os
import uvicorn

app = FastAPI(title="CyberTicket OpenEnv Backend")

env_state = {
    "tickets": [],
    "system_load": 0.0,
    "last_action_status": "None",
    "step_count": 0,
    "cumulative_reward": 0.0,
    "task_id": "task_categorization"
}

@app.get("/")
def read_root():
    return RedirectResponse(url='/docs')

@app.post("/reset")
def reset_env(config: Dict[str, Any] = None):
    global env_state
    config = config or {}
    env_state = {
        "tickets": config.get("initial_tickets", [{"id": "T1", "type": "Mixed"}]),
        "system_load": config.get("initial_load", 0.1),
        "last_action_status": "Environment reset.",
        "step_count": 0,
        "cumulative_reward": 0.0,
        "task_id": config.get("task_id", os.environ.get("TASK", "task_categorization"))
    }
    return get_state()

@app.post("/step")
def step_env(action: TicketAction):
    global env_state
    
    ticket = next((t for t in env_state["tickets"] if t["id"] == action.ticket_id), None)
    
    if not ticket:
        env_state["last_action_status"] = f"Error: Ticket {action.ticket_id} not found."
    else:
        if action.action_type == "categorize":
            ticket["category"] = action.value
            env_state["last_action_status"] = f"Categorized {action.ticket_id} as {action.value}."
        elif action.action_type == "set_priority":
            ticket["priority"] = action.value
            env_state["last_action_status"] = f"Set priority for {action.ticket_id} to {action.value}."
        elif action.action_type == "close_ticket":
            env_state["tickets"] = [t for t in env_state["tickets"] if t["id"] != action.ticket_id]
            env_state["last_action_status"] = f"Closed ticket {action.ticket_id}."

    env_state["step_count"] += 1
    env_state["system_load"] = min(1.0, float(len(env_state["tickets"]) * 0.1))

    task_id = os.environ.get("TASK", env_state.get("task_id", "task_categorization"))
    action_str = f"{action.action_type} {action.value}"
    
    grader_func = TASK_GRADERS.get(task_id, lambda x: 0.01)
    # Ensure float return value
    reward_val = float(grader_func(action_str))
    
    env_state["cumulative_reward"] += reward_val

    return {
        "observation": str(get_state().model_dump()),
        "reward": float(reward_val),
        "done": len(env_state["tickets"]) == 0,
        "info": {}
    }

@app.get("/state", response_model=TicketObs)
def get_state():
    return TicketObs(
        active_tickets=env_state["tickets"],
        system_load=env_state["system_load"],
        last_action_status=env_state["last_action_status"]
    )

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
