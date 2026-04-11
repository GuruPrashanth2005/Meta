def clamp(val): 
    return max(0.01, min(0.99, float(val)))

TASK_GRADERS = {
    "task_categorization": lambda x: clamp(0.99 if any(k in str(x).lower() for k in ["network", "hardware"]) else 0.01),
    "task_priority": lambda x: clamp(0.99 if any(k in str(x).lower() for k in ["high", "low"]) else 0.01),
    "task_resolution": lambda x: clamp(0.99 if len(str(x)) > 5 else 0.01)
}
