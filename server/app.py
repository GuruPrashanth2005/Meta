from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from server.models import TicketAction
from server.tasks import TASK_GRADERS
import os
import time
import uuid
import uvicorn

app = FastAPI(title="CyberTicket High-Performance Backend")

@app.get("/")
def read_root():
    return RedirectResponse(url='/docs')

@app.post("/reset")
def reset_env():
    return {"status": "Environment reset.", "memory_cleared": True}

@app.post("/step")
async def step_env(request: Request, action: TicketAction):
    # Concurrency tracker metrics
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
    
    # Capture latency dynamically for API logs
    latency_ms = (time.time() - start_time) * 1000
    
    return {
        "observation": f"RequestProcessed [ReqID:{req_id}] in {latency_ms:.3f}ms",
        "reward": float(reward_val),
        "done": True,
        "info": {
            "req_id": req_id,
            "latency_ms": latency_ms
        }
    }

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
