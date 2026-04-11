import re

def clamp(val): 
    return max(0.01, min(0.99, float(val)))

def elite_quality_score(text: str) -> float:
    """
    Quality Score evaluating:
    - Technical Accuracy (30%)
    - Professionalism & Empathy (40%)
    - Formatting/Structure (30%)
    """
    text_str = str(text)
    text_lower = text_str.lower()
    
    technical_score = 0.0
    professional_score = 0.0
    format_score = 0.0
    
    # Technical Accuracy (Max 0.30)
    tech_keywords = ["restart", "reboot", "configuration", "network", "hardware", "diagnostics", "latency", "bandwidth", "firewall", "patch"]
    matches = sum(1 for w in tech_keywords if w in text_lower)
    if matches >= 2:
        technical_score = 0.30
    elif matches == 1:
        technical_score = 0.15
        
    # Professionalism & Empathy (Max 0.40)
    prof_keywords = ["please", "thank", "apologize", "understand", "patience", "glad", "assist", "resolution", "empathy"]
    prof_matches = sum(1 for w in prof_keywords if w in text_lower)
    if prof_matches >= 2:
        professional_score = 0.40
    elif prof_matches == 1:
        professional_score = 0.20
        
    # Formatting (Max 0.30)
    # Check for diagnostic template elements
    if "resolution code:" in text_lower or re.search(r'[A-Z]{2,3}-\d{2,4}', text_str):
        format_score += 0.15
    if "<scratchpad>" in text_lower or "diagnostic:" in text_lower or "action:" in text_lower:
        format_score += 0.15
        
    total_score = technical_score + professional_score + format_score
    
    # Base padding to prevent zero
    if total_score < 0.01:
        return 0.01
        
    return clamp(total_score)

TASK_GRADERS = {
    "task_1": elite_quality_score,
    "task_2": elite_quality_score,
    "task_3": elite_quality_score
}
