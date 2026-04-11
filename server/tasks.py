import math
import re

def clamp(val):
    return max(0.01, min(0.99, float(val)))

def multi_factor_scorer(text: str) -> float:
    """
    High-Performance Heuristic Engine:
    - Factor A: Keyword density (25%)
    - Factor B: Sentence structure entropy (25%)
    - Factor C: Astra-Flux nomenclature adherence (50%)
    """
    text_str = str(text)
    text_lower = text_str.lower()
    words = text_lower.split()
    
    if not words:
        return 0.01
        
    factor_a = 0.0
    factor_b = 0.0
    factor_c = 0.0
    
    # Factor A (25%)
    tech_keywords = {"network", "hardware", "firewall", "server", "reboot", "patch", "latency", "configuration", "diagnostic"}
    keyword_count = sum(1 for w in words if w in tech_keywords)
    density = keyword_count / len(words)
    factor_a = min(0.25, (density / 0.1) * 0.25)
    
    # Factor B (25%)
    freq_dict = {}
    for w in words:
        freq_dict[w] = freq_dict.get(w, 0) + 1
    entropy = -sum((count / len(words)) * math.log2(count / len(words)) for count in freq_dict.values())
    factor_b = min(0.25, (entropy / 4.0) * 0.25) 
    
    # Factor C (50%)
    if "astra-flux" in text_lower or "astra" in text_lower:
        factor_c += 0.20
    if re.search(r'[A-Z]{2,4}-\d{2,4}', text_str):
        factor_c += 0.30
        
    total_score = factor_a + factor_b + factor_c + 0.01
    return clamp(total_score)

TASK_GRADERS = {
    "task_1": multi_factor_scorer,
    "task_2": multi_factor_scorer,
    "task_3": multi_factor_scorer
}
