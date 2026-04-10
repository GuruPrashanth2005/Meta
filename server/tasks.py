from typing import Dict, Any

class BaseTask:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    def get_initial_state(self):
        return {"initial_tickets": [], "initial_load": 0.0}
        
    def grader(self, trajectory: list) -> float:
        return 0.01

class CategorizeTicketTask(BaseTask):
    def get_initial_state(self):
        return {
            "initial_tickets": [{"id": "T1", "desc": "Forgot password", "type": "Password Reset"}], 
            "initial_load": 0.1
        }
        
    def grader(self, trajectory: list) -> float:
        action_count = sum(1 for step in trajectory if step.get("action") and step["action"].get("action_type") == "categorize")
        if action_count == 0:
            return 0.01  # wrong
        elif action_count == 1:
            return 0.99  # perfect
        else:
            return 0.5   # partially right if they did too many or something else

class PriorityAssignmentTask(BaseTask):
    def get_initial_state(self):
        return {
            "initial_tickets": [{"id": "T1", "desc": "DB down", "type": "Server Down"}], 
            "initial_load": 0.5
        }
        
    def grader(self, trajectory: list) -> float:
        action_count = sum(1 for step in trajectory if step.get("action") and step["action"].get("action_type") == "set_priority")
        if action_count == 0:
            return 0.01  # wrong
        elif action_count == 1:
            return 0.99  # perfect
        else:
            return 0.5   # partially right

class ResolutionDraftTask(BaseTask):
    def get_initial_state(self):
        return {
            "initial_tickets": [{"id": f"T{i}", "desc": f"Issue {i}", "type": "Mixed"} for i in range(1, 11)], 
            "initial_load": 0.9
        }
        
    def grader(self, trajectory: list) -> float:
        closed = sum(1 for step in trajectory if step.get("action") and step["action"].get("action_type") == "close_ticket")
        if closed == 0:
            return 0.01  # wrong
        elif closed == 10:
            return 0.99  # perfect
        else:
            return 0.5   # partially right
