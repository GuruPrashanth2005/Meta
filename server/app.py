from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from server.models import TicketAction
from server.tasks import TASK_GRADERS
import os
import uvicorn

app = FastAPI(title="Scaler SST CyberTicket Elite Backend")

# Context Buffer to track conversation history per session
CONTEXT_BUFFER = {
    "step_count": 0,
    "session_memory": [],
    "cumulative_reward": 0.0,
}

@app.get("/")
def read_root():
    return RedirectResponse(url='/docs')

@app.post("/reset")
def reset_env():
    global CONTEXT_BUFFER
    CONTEXT_BUFFER = {
        "step_count": 0,
        "session_memory": [],
        "cumulative_reward": 0.0,
    }
    return {"status": "Environment reset.", "memory_cleared": True}

@app.post("/step")
async def step_env(request: Request, action: TicketAction):
    global CONTEXT_BUFFER
    
    try:
        body = await request.json()
    except Exception:
        body = {}
        
    task_id = body.get("task_id", action.task_id or "task_1")
    action_str = f"{action.action_type} {action.value}"
    
    grader_func = TASK_GRADERS.get(task_id, lambda x: 0.01)
    reward_val = float(grader_func(action_str))
    
    # Update Context Buffer
    CONTEXT_BUFFER["step_count"] += 1
    CONTEXT_BUFFER["cumulative_reward"] += reward_val
    CONTEXT_BUFFER["session_memory"].append({
        "task": task_id,
        "action": action_str,
        "reward": reward_val
    })

    return {
        "observation": f"Action processed. Current buffer depth: {len(CONTEXT_BUFFER['session_memory'])}",
        "reward": float(reward_val),
        "done": True,
        "info": {"context_memory": CONTEXT_BUFFER["session_memory"]}
    }

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
