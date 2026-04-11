def clamp_score(score):
    return max(0.01, min(0.99, float(score)))

TASK_GRADERS = {
    "task_categorization": lambda x: clamp_score(0.99 if "network" in x.lower() else 0.01),
    "task_priority": lambda x: clamp_score(0.99 if "high" in x.lower() else 0.01),
    "task_resolution": lambda x: clamp_score(0.99 if "reset" in x.lower() else 0.01)
}
