from typing import Dict, Any

class BaseTask:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    def get_initial_state(self):
        return {"initial_tickets": [], "initial_load": 0.0}
    def grader(self, trajectory: list) -> float:
        return 0.0

class CategorizeTask(BaseTask):
    def get_initial_state(self):
        return {"initial_tickets": [{"id": "T1", "desc": "Forgot password", "type": "Password Reset"}], "initial_load": 0.1}
    def grader(self, trajectory: list) -> float:
        return min(1.0, sum(0.2 for step in trajectory if step["action"]["action_type"] == "categorize"))

class PriorityTask(BaseTask):
    def get_initial_state(self):
        return {"initial_tickets": [{"id": "T1", "desc": "DB down", "type": "Server Down"}], "initial_load": 0.5}
    def grader(self, trajectory: list) -> float:
        return min(1.0, sum(0.5 for step in trajectory if step["action"]["action_type"] == "set_priority"))

class ResolutionTask(BaseTask):
    def get_initial_state(self):
        return {"initial_tickets": [{"id": f"T{i}", "desc": f"Issue {i}", "type": "Mixed"} for i in range(1, 11)], "initial_load": 0.9}
    def grader(self, trajectory: list) -> float:
        closed = sum(1 for step in trajectory if step["action"]["action_type"] == "close_ticket")
        return min(1.0, closed * 0.1)
