import math
import re

def clamp(val):
    return max(0.01, min(0.99, float(val)))

def semantic_density_scorer(text: str) -> float:
    """
    Semantic Density Scoring Engine
    - Factor A: Technical Specificity (Regex check for AF-XXXX)
    - Factor B: Sentence Entropy (Diverse, professional vocabulary)
    - Factor C: Policy Adherence (Resolution isn't generic)
    """
    text_str = str(text)
    text_lower = text_str.lower()
    words = text_lower.split()
    
    if not words: return 0.01
    
    # Factor A: Technical Specificity (Regex check for AF-XXXX series protocols)
    factor_a = 0.0
    if re.search(r'AF-\d{4}\b', text_str):
        factor_a += 0.33
        
    # Factor B: Sentence Entropy (Reward diverse, professional vocabulary)
    freq_dict = {}
    for w in words:
        freq_dict[w] = freq_dict.get(w, 0) + 1
    entropy = -sum((count / len(words)) * math.log2(count / len(words)) for count in freq_dict.values())
    
    sentiment_keywords = {"apologize", "patience", "assist", "glad", "understand", "efficient", "resolved", "swift", "optimal", "flux"}
    professional_bonus = min(0.10, sum(1 for w in words if w in sentiment_keywords) * 0.05)
    
    factor_b = min(0.33, ((max(0.0, entropy) / 5.0) * 0.23) + professional_bonus)
    
    # Factor C: Policy Adherence (Verify the resolution isn't generic)
    generic_phrases = ["generic", "placeholder", "test dummy", "lorem ipsum", "default response"]
    is_generic = any(g in text_lower for g in generic_phrases)
    factor_c = 0.00 if is_generic else 0.33
    
    final_score = factor_a + factor_b + factor_c
    return clamp(final_score)

TASK_GRADERS = {
    "task_1": semantic_density_scorer,
    "task_2": semantic_density_scorer,
    "task_3": semantic_density_scorer,
    "task_categorization": semantic_density_scorer, 
    "task_priority": semantic_density_scorer,
    "task_resolution": semantic_density_scorer
}
