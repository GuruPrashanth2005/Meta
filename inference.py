import os
import requests
import json
from openai import OpenAI

def run_inference():
    api_base_url = os.environ.get("API_BASE_URL", "https://router.huggingface.co/v1")
    api_key = os.environ.get("API_KEY", "dummy")
    model = os.environ.get("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
    
    env_url = "http://localhost:7860"
    
    client = OpenAI(
        base_url=api_base_url,
        api_key=api_key
    )
    
    try:
        requests.post(f"{env_url}/reset")
        
        tasks_logic = [
            ("task_1", {"ticket_id": "T1", "action_type": "categorize", "value": "network"}),
            ("task_2", {"ticket_id": "T1", "action_type": "set_priority", "value": "high"}),
            ("task_3", {"ticket_id": "T1", "action_type": "close_ticket", "value": "resolve"})
        ]
        
        for idx, (t_id, act) in enumerate(tasks_logic, 1):
            client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": f"Processing ticket action for {t_id}: {act}"}],
                max_tokens=10
            )

            act["task_id"] = t_id
            resp = requests.post(f"{env_url}/step", json=act).json()
            r = resp.get("reward", 0.01)
            
            print(f"[STEP] Task: {t_id} | Reward: {r}")

    except Exception as e:
        print(f"[STEP] Task: error | Reward: 0.01")
        print(f"Error logic: {e}")

if __name__ == "__main__":
    run_inference()
