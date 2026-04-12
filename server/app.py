from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from server.models import TicketAction
from server.tasks import TASK_GRADERS
import os
import time
import uuid
import uvicorn

app = FastAPI(title="Astra Flux Scalable Backend - Async & Global State")

# Global context dictionary to maintain state across tasks
GLOBAL_CONTEXT = {
    "session_id": str(uuid.uuid4()),
    "task_history": [],
    "total_interactions": 0,
    "system_status": "resource limits active (2 vCPU / 8 GB RAM)"
}

@app.get("/")
async def read_root():
    return RedirectResponse(url='/docs')

@app.post("/reset")
async def reset_env():
    global GLOBAL_CONTEXT
    GLOBAL_CONTEXT["session_id"] = str(uuid.uuid4())
    GLOBAL_CONTEXT["task_history"] = []
    GLOBAL_CONTEXT["total_interactions"] = 0
    return {"status": "Environment reset.", "context_cleared": True}

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
    
    GLOBAL_CONTEXT["total_interactions"] += 1
    GLOBAL_CONTEXT["task_history"].append({
        "req_id": req_id,
        "task_id": task_id,
        "reward": reward_val,
        "action": action_str
    })
    
    latency_seconds = time.time() - start_time
    latency_ms = latency_seconds * 1000.0
    
    return {
        "observation": f"Request processed efficiently. Current Interaction Depth: {GLOBAL_CONTEXT['total_interactions']}",
        "reward": float(reward_val),
        "done": True,
        "info": {
            "req_id": req_id,
            "latency_ms": f"{latency_ms:.4f}",
            "session_id": GLOBAL_CONTEXT["session_id"]
        }
    }

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
