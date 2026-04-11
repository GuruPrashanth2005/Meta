import re

def clamp(val): 
    return max(0.01, min(0.99, float(val)))

def heuristic_grader(text: str) -> float:
    """
    Advanced Heuristic Grader checking for:
    - Minimum word count
    - Professional tone
    - Formal Resolution Code (e.g., AF-99)
    """
    text_str = str(text)
    text_lower = text_str.lower()
    words = text_lower.split()
    
    # Lazy answer penalty
    if len(words) < 5:
        return clamp(0.01)
        
    score = 0.4
    
    # Professional tone bonus
    professional_keywords = ["please", "thank", "assist", "resolve", "apologize", "update", "priority", "network", "hardware"]
    if sum(1 for w in professional_keywords if w in text_lower) >= 1:
        score += 0.25
        
    # Resolution code bonus (e.g., AF-99, INC-123)
    if re.search(r'[A-Z]{2,3}-\d{2,4}', text_str):
        score += 0.35
        
    return clamp(score)

TASK_GRADERS = {
    "task_1": heuristic_grader,
    "task_2": heuristic_grader,
    "task_3": heuristic_grader
}
