# 🤖 AI Code Reviewer & Benchmark Tool (Local LLMs)

This project is a **Source Code Analysis and Performance Benchmarking Tool** leveraging Large Language Models (LLMs) running entirely offline (localhost).

The tool enables users to compare the **bug detection capabilities** (Logic, Syntax, Security) and **processing speed** of lightweight models such as **Yi-Coder**, **Qwen2.5-Coder**, and **Llama 3.2**.

---

## 🚀 Key Features

1.  **AI Code Review (Chat Mode):**
    * Automatically detects bugs and suggests fixes.
    * Supports multiple languages: Python, Java, C/C++, etc.
    * **Side-by-side comparison**: View results from 3 models simultaneously.

2.  **Performance Benchmark (Auto-Test):**
    * Integrated **"Nightmare Mode" Test Suite** (20+ cases): Covers complex issues like Deadlocks, Race Conditions, Memory Leaks, and SQL Injection.
    * Precise **Latency Measurement** (Cold-start).
    * Automatic **Visualization** (Bar charts and Dataframes).

3.  **Technology Stack:**
    * **Backend AI:** Ollama (Running GGUF models offline).
    * **Frontend:** Streamlit (Python).
    * **Deployment:** Docker & Docker Compose.

---

## 🛠️ Installation & Usage (Docker - Recommended)

This is the fastest way to run the project without manually installing Python or Ollama.

### Step 1: Start Services
Open your terminal in the project directory and run:

```bash
docker-compose up -d
```

### Step 2: Download AI Models (First time only)
Once the containers are running, you need to pull the models into the Ollama container. Run these commands one by one:

```bash
docker exec -it ollama_backend ollama pull yi-coder:1.5b
docker exec -it ollama_backend ollama pull qwen2.5-coder:1.5b
docker exec -it ollama_backend ollama pull llama3.2:1b
```

### Step 3: Access the App
Open your browser and navigate to: 👉 http://localhost:8501

## 💻 Manual Installation (No Docker)

If you prefer running it directly on your machine (requires Python 3.8+ and Ollama installed):

### Install Python Dependencies:
```bash
pip install -r requirements.txt
```

### Pull Models (via Ollama):
```bash
ollama pull yi-coder:1.5b
ollama pull qwen2.5-coder:1.5b
ollama pull llama3.2:1b
```

### Run the App:
```bash
streamlit run app.py
```

## 📊 Benchmark Methodology

The project utilizes a Hardcoded Test Suite (embedded in app.py and benchmark_notebook.ipynb) to evaluate models based on:
- **Performance**: Time taken from request to response (measured in seconds).
- **Quality (Human Evaluation)**: The ability to identify subtle and critical bugs, including:
  - Python: Algorithmic Logic (Knapsack, Binary Search), Security (Pickle RCE).
  - Java: Concurrency issues (Deadlock, Race Condition).
  - C/C++: Memory management (Double Free, Buffer Overflow).

## 📂 Project Structure

```
.
├── app.py                   # Main Application (Streamlit)
├── benchmark_notebook.ipynb # Jupyter Notebook for in-depth analysis
├── docker-compose.yml       # Docker services orchestration
├── Dockerfile               # Docker build instructions for the App
├── requirements.txt         # Python dependencies
└── README.md                # Documentation
```
