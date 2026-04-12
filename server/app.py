from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from server.models import TicketAction
from server.tasks import TASK_GRADERS
import os
import time
import uuid
import uvicorn

app = FastAPI(title="Scaler SST Astra Flux God-Tier Backend")

GLOBAL_SESSION_MEMORY = {
    "history": [],
    "total_queries": 0
}

@app.get("/")
def read_root():
    return RedirectResponse(url='/docs')

@app.post("/reset")
def reset_env():
    global GLOBAL_SESSION_MEMORY
    GLOBAL_SESSION_MEMORY = {
        "history": [],
        "total_queries": 0
    }
    return {"status": "Environment reset.", "memory_cleared": True}

@app.post("/step")
async def step_env(request: Request, action: TicketAction):
    req_id = str(uuid.uuid4())
    start_time = time.time()
    
    try:
        body = await request.json()
    except Exception:
        body = {}
        
    task_id = body.get("task_id", action.task_id or "task_1")
    action_str = f"{action.action_type} {action.value}"
    
    grader_func = TASK_GRADERS.get(task_id, lambda x: 0.01)
    reward_val = float(grader_func(action_str))
    
    GLOBAL_SESSION_MEMORY["total_queries"] += 1
    GLOBAL_SESSION_MEMORY["history"].append({
        "req_id": req_id,
        "task_id": task_id,
        "reward": reward_val
    })
    
    latency_seconds = time.time() - start_time
    latency_ms = latency_seconds * 1000.0
    
    return {
        "observation": f"Processed gracefully. Sequence Depth: {GLOBAL_SESSION_MEMORY['total_queries']}",
        "reward": float(reward_val),
        "done": True,
        "info": {
            "req_id": req_id,
            "latency_ms": f"{latency_ms:.4f}"
        }
    }

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
