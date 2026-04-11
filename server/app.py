from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from server.models import TicketAction
from server.tasks import TASK_GRADERS
import os
import uvicorn

app = FastAPI(title="Enterprise CyberTicket Backend")

# Session Manager to track agent accuracy trends over time
SESSION_MANAGER = {
    "step_count": 0,
    "cumulative_reward": 0.0,
    "reward_history": [],
    "trend": "neutral"
}

@app.get("/")
def read_root():
    return RedirectResponse(url='/docs')

@app.post("/reset")
def reset_env():
    global SESSION_MANAGER
    SESSION_MANAGER = {
        "step_count": 0,
        "cumulative_reward": 0.0,
        "reward_history": [],
        "trend": "neutral"
    }
    return {"status": "Environment reset.", "session": SESSION_MANAGER}

@app.post("/step")
async def step_env(request: Request, action: TicketAction):
    global SESSION_MANAGER
    
    try:
        body = await request.json()
    except Exception:
        body = {}
        
    task_id = body.get("task_id", action.task_id or "task_1")
    action_str = f"{action.action_type} {action.value}"
    
    grader_func = TASK_GRADERS.get(task_id, lambda x: 0.01)
    reward_val = float(grader_func(action_str))
    
    # Internal Session tracking
    SESSION_MANAGER["step_count"] += 1
    SESSION_MANAGER["cumulative_reward"] += reward_val
    SESSION_MANAGER["reward_history"].append(reward_val)
    
    history_len = len(SESSION_MANAGER["reward_history"])
    if history_len > 1:
        prev = SESSION_MANAGER["reward_history"][-2]
        if reward_val > prev:
            SESSION_MANAGER["trend"] = "improving"
        elif reward_val < prev:
            SESSION_MANAGER["trend"] = "degrading"
        else:
            SESSION_MANAGER["trend"] = "stable"

    return {
        "observation": f"success_trend_{SESSION_MANAGER['trend']}",
        "reward": float(reward_val),
        "done": True,
        "info": {"session_trend": SESSION_MANAGER["trend"]}
    }

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
