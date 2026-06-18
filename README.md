# 📝 AI Question Paper Generator

An AI-powered assessment engineering system designed to automatically extract core pedagogical concepts from text or uploaded documents and generate highly targeted examination papers (MCQs, short-answer, and long-answer questions) based on user-defined difficulty levels.

## 🚀 Live Demo
🔗 **[Insert your live Streamlit Cloud URL here]**

---

## ✨ Key Features
* **Dual Input Modalities:** Supports seamless text-based material processing along with robust native PDF text extraction.
* **Taxonomy-Based Control:** Leverages Large Language Models to contextually analyze content and structure parameters for **Easy**, **Medium**, or **Hard** evaluations.
* **Granular Question Orchestration:** Empowers users to balance paper blueprints with sliders configuring precise numbers of Multiple Choice Questions (MCQs), Short-Answer, and Long-Answer prompts.
* **Structured Output & Evaluation Metrics:** Enforces deterministic JSON schemas directly through backend LLM prompting to extract exact grading keys, marking rubrics, and conceptual evaluation checkpoints.
* **Interactive Evaluation Panel:** Clean UI utilizing tab-based content views with intuitive accordion drop-downs to reveal answer guidelines for test-makers.
* **Data Portability:** Single-click feature allowing creators to download the finalized examination metrics as a formatted JSON schema payload.

---

## 🛠️ Tech Stack & Architecture

* **Frontend Framework:** Streamlit (Persistently state-managed dashboard runtime)
* **Core NLP Engine & LLM:** Google Gemini API (`gemini-1.5-flash-latest` variant)
* **Document Processing Engine:** PyPDF (Binary extraction parsing layer)
* **Backend Runtime:** Python 3.x
* **Data Serialization:** Strict JSON Scheme Mapping

---

## 💻 Local Setup & Installation

### 1. Clone the Workspace
```bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME
