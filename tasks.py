from typing import Dict, Any

class BaseTask:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def get_initial_state(self):
        return {"initial_tickets": [], "initial_load": 0.0}

    def grader(self, trajectory: list) -> float:
        return 0.0

class EasyTask(BaseTask):
    """Categorize 3 'Password Reset' tickets correctly."""
    def get_initial_state(self):
        return {
            "initial_tickets": [
                {"id": "T1", "desc": "Forgot password for email", "type": "Password Reset"},
                {"id": "T2", "desc": "Domain account locked out", "type": "Password Reset"},
                {"id": "T3", "desc": "Need VPN password reset", "type": "Password Reset"}
            ],
            "initial_load": 0.3
        }

    def grader(self, trajectory: list) -> float:
        score = 0.0
        categories_done = sum(1 for step in trajectory if step["action"]["action_type"] == "categorize" and step["action"]["value"] == "Password Reset")
        score += min(categories_done * 0.2, 0.6)
        return min(score, 1.0)

class MediumTask(BaseTask):
    """Prioritize 'Server Down' tickets over 'Printer Jam' and assign to the 'Admin' user."""
    def get_initial_state(self):
        return {
            "initial_tickets": [
                {"id": "T1", "desc": "Printer paper jam on floor 3", "type": "Printer Jam"},
                {"id": "T2", "desc": "Main database server is down", "type": "Server Down"}
            ],
            "initial_load": 0.5
        }

    def grader(self, trajectory: list) -> float:
        score = 0.0
        escalated_admin = any(step["action"]["action_type"] == "escalate" and step["action"]["value"] == "Admin" and step["action"]["ticket_id"] == "T2" for step in trajectory)
        if escalated_admin:
            score += 0.5
        closed_all = sum(1 for step in trajectory if step["action"]["action_type"] == "close") == 2
        if closed_all:
            score += 0.5
        return min(score, 1.0)


class HardTask(BaseTask):
    """Resolve a mixed queue of 10 tickets, maintaining system load below 80% and prioritizing by SLA."""
    def get_initial_state(self):
        tickets = [{"id": f"T{i}", "desc": f"Mixed issue {i}", "type": "Mixed"} for i in range(1, 11)]
        return {
            "initial_tickets": tickets,
            "initial_load": 0.9 # High load initially to test reduction
        }

    def grader(self, trajectory: list) -> float:
        score = 0.0
        closed_count = sum(1 for step in trajectory if step["action"]["action_type"] == "close")
        score += min(closed_count * 0.1, 1.0)
        
        # Check if load stayed below 80%
        load_ok = all(step["obs"]["system_load"] < 0.8 for step in trajectory)
        if not load_ok:
            score = max(0.0, score - 0.5)
            
        return min(score, 1.0)
