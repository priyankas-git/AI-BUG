# AI Bug Detection and Auto-Remediation Tool

An AI-powered Bug Detection and Auto-Remediation platform. The system allows developers to submit source code, analyze it using a combination of static analysis and Generative AI, detect potential bugs, classify them, assign severity and confidence, explain the problem, generate a suggested fix, and validate the fix.

---

## Folder Structure

All project files reside inside the `AI-BUG-DETECTION/` folder:

```text
AI-BUG-DETECTION/
│
├── backend/            # FastAPI backend logic (services, models, prompt managers)
├── frontend/           # Streamlit multi-page interface (Dashboard, Analysis, Bugs, Remediation)
├── sample-code/        # Sample buggy code blocks for testing (Python & JavaScript)
│
├── README.md           # Project folder instructions
└── .gitignore          # Global git ignore configuration
```

---

## Technology Stack

- **Core**: Python 3.10+
- **AI Orchestration**: LangChain + LangChain OpenAI (`ChatOpenAI`)
- **LLM Provider**: OpenAI (GPT-4o or configured model)
- **Frontend Dashboard**: Streamlit (Multi-page configuration)
- **Database & Persistence**: SQLite prototype database with SQLAlchemy ORM
- **AST / Parser Checks**: Python Abstract Syntax Tree (AST) modules

---

## Quick Start Setup

### Step 1: Clone and Configure Environment

1. Navigate to the backend directory and create a virtual environment:
   ```bash
   cd AI-BUG-DETECTION/backend
   python -m venv venv
   ```
2. Activate the virtual environment:
   - **Windows PowerShell**: `venv\Scripts\activate`
   - **macOS/Linux**: `source venv/bin/activate`
3. Install dependencies:
   ```bash
   pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org --trusted-host pypi.python.org
   ```
4. Create a `.env` file from the template (`.env.example`) and fill in your keys:
   ```env
   OPENAI_API_KEY=your-api-key-here
   OPENAI_MODEL=gpt-4o
   ```
5. Initialize the database schema:
   ```bash
   python -m database.init_db
   ```

### Step 2: Start the Frontend Interface

The frontend is a Python Streamlit app that connects directly to the backend services.

1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```
2. Install frontend specific dependencies (Plotly, etc.) inside the activated environment:
   ```bash
   pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org --trusted-host pypi.python.org
   ```
3. Run the Streamlit application:
   ```bash
   streamlit run Dashboard.py
   ```
4. Open your browser to the local URL (usually `http://localhost:8501`).

---

## Team Structure & Owner Matrix

### BACKEND — 2 People
1. **Disha** (AI Bug Detection Engine):
   - `backend/services/ai_analyzer.py`
   - `backend/services/bug_classifier.py`
   - `backend/services/severity_engine.py`
   - `backend/services/fix_generator.py`
   - `backend/services/prompt_manager.py`
   - `backend/prompts/`
2. **Pavan** (API + Static Analysis + Database):
   - `backend/main.py`
   - `backend/routes/`
   - `backend/services/static_analyzer.py`
   - `backend/services/result_fusion.py`
   - `backend/services/validation_service.py`
   - `backend/models/`
   - `backend/schemas/`
   - `backend/database/`
   - `backend/utils/`
   - `backend/tests/`

### FRONTEND — 3 People
3. **Afreen** (Dashboard + Analytics):
   - `frontend/Dashboard.py`
4. **Rithi** (Code Analysis + Code Editor):
   - `frontend/pages/1_Code_Analysis.py`
5. **Priyanka** (Bug Details + Fix/Validation + UI Integration):
   - `frontend/pages/2_Bugs_List.py`
   - `frontend/pages/3_Remediation_Studio.py`
