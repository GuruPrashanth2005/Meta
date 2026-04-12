# 🌌 Astra Flux: Self-Correcting Agentic System  
**Meta PyTorch OpenEnv Hackathon**

[![Status: Validated](https://img.shields.io/badge/Phase_2-Passed-green.svg)](#) 
[![Python: 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](#)
[![License: MIT](https://img.shields.io/badge/license-MIT-lightgrey.svg)](#)

Astra Flux is a high-fidelity agentic environment designed for the **Meta OpenEnv Challenge**. It solves the "Stochastic Hallucination" problem in LLMs by implementing a recursive **Alignment Critic** loop, ensuring all infrastructure resolutions follow strict **AF-Protocol** standards.

---

## 🏆 Scoring & Performance Matrix

| Category | Weight | Implementation Detail |
| :--- | :--- | :--- |
| **Real-World Utility** | **30%** | Simulates SRE workflows using 100+ AF-series technical protocols |
| **Grader Quality** | **25%** | Multi-factor heuristic using Shannon Entropy & Regex Density |
| **Env Design** | **20%** | Stateful FastAPI backend with async session persistence |
| **Code Quality** | **15%** | Spec-perfect OpenAI Client integration & root-level inference |
| **Creativity** | **10%** | Dual-pass "Self-Critique" agentic reasoning engine |

---

## 🧠 System Architecture

Astra Flux operates on a **closed-loop feedback system**. Instead of a single-pass inference, the agent undergoes a self-audit before committing an action to the environment.

### 1. The Alignment Critic Loop

1. **Inference (Draft):** Agent generates a resolution for an AF-series ticket  
2. **Critique (Audit):** Secondary internal logic checks for nomenclature errors or policy violations  
3. **Refinement:** Regenerates action if audit fails  
4. **Execution:** Refined action is POSTed to the environment server on port `7860`  

---

### 2. Semantic Density Math

The environment server rewards agents based on **Information Density**:

$$
R = \max(0.01, \min(0.99, (S_{tech} \cdot 0.5 + S_{entropy} \cdot 0.3 + S_{policy} \cdot 0.2)))
$$

- **Technical Density ($S_{tech}$):** Validates AF-XXXX protocol patterns via regex  
- **Vocabulary Entropy ($S_{entropy}$):** Rewards diverse, professional wording  
- **Alignment Policy ($S_{policy}$):** Penalizes generic or low-effort responses  

---

## 📂 Project Structure

```text
.
├── inference.py       # Core Agent Logic & Alignment Critic (OpenAI Client)
├── server/
│   ├── app.py         # Async Environment Backend (FastAPI)
│   └── tasks.py       # Semantic Density Grader & Scoring Engine
├── requirements.txt   # Dependencies
└── README.md          # Documentation
```

---

## 🚀 Deployment & Spec Compliance

### Technical Requirements

- **Entry Point:** `inference.py` (Root Directory)  
- **SDK:** OpenAI Python SDK (Mandatory)  
- **Port Mapping:** `7860` (Hugging Face Compatible)  
- **Resources:** 2 vCPU / 8 GB RAM  

---

### Environment Variables

```bash
export HF_TOKEN="your_huggingface_token"
export API_BASE_URL="your_meta_endpoint_url"
export MODEL_NAME="gpt-4.1-mini"
```

---

### 📡 Logging Protocol

```text
[START] task=ID env=astra-flux model=NAME

[STEP] step=1 action='...' reward=0.XX done=true error=null

[END] success=true steps=1 rewards=0.XX
```
---

## 👨‍💻 Author

**Guru Prashanth S**  
Validated for the **Meta PyTorch x Scaler SST Grand Finale**

## 🤝 Contributors

- **Balamithra D**  
- **Pavithra R**
