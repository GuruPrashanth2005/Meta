from typing import Dict, Any

class BaseTask:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    def get_initial_state(self):
        return {"initial_tickets": [], "initial_load": 0.0}
    def grader(self, trajectory: list) -> float:
        return 0.01

def clamp_score(score: float) -> float:
    return max(0.01, min(0.99, score))

class CategorizeTicketTask(BaseTask):
    def get_initial_state(self):
        return {"initial_tickets": [{"id": "T1", "desc": "Forgot password", "type": "Password Reset"}], "initial_load": 0.1}
    def grader(self, trajectory: list) -> float:
        score = sum(0.99 for step in trajectory if step.get("action") and step["action"].get("action_type") == "categorize")
        return clamp_score(score)

class PriorityAssignmentTask(BaseTask):
    def get_initial_state(self):
        return {"initial_tickets": [{"id": "T1", "desc": "DB down", "type": "Server Down"}], "initial_load": 0.5}
    def grader(self, trajectory: list) -> float:
        score = sum(0.99 for step in trajectory if step.get("action") and step["action"].get("action_type") == "set_priority")
        return clamp_score(score)

class ResolutionDraftTask(BaseTask):
    def get_initial_state(self):
        return {"initial_tickets": [{"id": f"T{i}", "desc": f"Issue {i}", "type": "Mixed"} for i in range(1, 11)], "initial_load": 0.9}
    def grader(self, trajectory: list) -> float:
        closed = sum(1 for step in trajectory if step.get("action") and step["action"].get("action_type") == "close_ticket")
        return clamp_score(closed * 0.1)
