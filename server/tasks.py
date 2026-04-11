def clamp(val): 
    return max(0.01, min(0.99, float(val)))

TASK_GRADERS = {
    "task_1": lambda x: clamp(0.99 if "network" in str(x).lower() else 0.01),
    "task_2": lambda x: clamp(0.99 if "high" in str(x).lower() else 0.01),
    "task_3": lambda x: clamp(0.99 if "resolve" in str(x).lower() else 0.01)
}
