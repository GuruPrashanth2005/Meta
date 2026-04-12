import math
import re

def clamp(val):
    return max(0.01, min(0.99, float(val)))

def quantum_heuristic_grader(text: str) -> float:
    """
    God-Tier Heuristic Engine evaluating:
    - Technical Specificity (40%)
    - Professional Sentiment (30%)
    - Structural Entropy (30%)
    """
    text_str = str(text)
    text_lower = text_str.lower()
    words = text_lower.split()
    
    if not words: return 0.01
    
    # Factor A: Technical Specificity (Max 0.40)
    factor_a = 0.0
    if "flux" in text_lower:
        factor_a += 0.20
    # Match AF-100 to AF-9999
    if re.search(r'AF-[1-9]\d{2,3}\b', text_str):
        factor_a += 0.20
        
    # Factor B: Professional Sentiment (Max 0.30)
    sentiment_keywords = {"apologize", "patience", "assist", "glad", "understand", "efficient", "resolved", "swift", "optimal"}
    sentiment_count = sum(1 for w in words if w in sentiment_keywords)
    factor_b = min(0.30, sentiment_count * 0.10)
    
    # Factor C: Structural Entropy (Max 0.30)
    freq_dict = {}
    for w in words:
        freq_dict[w] = freq_dict.get(w, 0) + 1
    entropy = -sum((count / len(words)) * math.log2(count / len(words)) for count in freq_dict.values())
    factor_c = min(0.30, (entropy / 4.5) * 0.30)
    
    total_score = factor_a + factor_b + factor_c + 0.01
    return clamp(total_score)

TASK_GRADERS = {
    "task_1": quantum_heuristic_grader,
    "task_2": quantum_heuristic_grader,
    "task_3": quantum_heuristic_grader,
    "task_categorization": quantum_heuristic_grader, 
    "task_priority": quantum_heuristic_grader,
    "task_resolution": quantum_heuristic_grader
}
