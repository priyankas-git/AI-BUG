# AI Bug Detection and Auto-Remediation Tool

An AI-powered Bug Detection and Auto-Remediation platform. The system allows developers to submit source code, analyze it using a combination of static analysis and Generative AI, detect potential bugs, classify them, assign severity and confidence, explain the problem, generate a suggested fix, and validate the fix.

## Architecture

The project is split into two independent services:
- **Backend**: FastAPI web server with SQLite database, Python AST/static analyzers, and Generative AI service abstraction.
- **Frontend**: React application bundled with Vite, styled with Tailwind CSS, using Monaco Editor for code editing and Recharts for analytics.

---

## Folder Structure

```text
AI-BUG-DETECTION/
│
├── backend/            # FastAPI Backend
├── frontend/           # React Frontend
├── sample-code/        # Sample buggy files for testing
│   ├── python/
│   └── javascript/
│
├── README.md           # Root README
└── .gitignore          # Git Ignore file
```

---

## Team Structure & Ownership

### BACKEND (2 People)
1. **Disha** — AI Bug Detection Engine
   - `backend/services/ai_analyzer.py`
   - `backend/services/bug_classifier.py`
   - `backend/services/severity_engine.py`
   - `backend/services/fix_generator.py`
   - `backend/services/prompt_manager.py`
   - `backend/prompts/`
2. **Pavan** — API, Static Analysis, Database
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

### FRONTEND (3 People)
3. **Afreen** — Dashboard + Analytics
   - `frontend/src/pages/Dashboard.jsx`
   - `frontend/src/components/dashboard/`
4. **Rithi** — Code Analysis + Code Editor
   - `frontend/src/pages/AnalysisPage.jsx`
   - `frontend/src/components/analysis/`
   - `frontend/src/hooks/useAnalysis.js`
5. **Priyanka** — Bug Details + Fix/Validation + UI Integration
   - `frontend/src/pages/BugsPage.jsx`
   - `frontend/src/pages/BugDetails.jsx`
   - `frontend/src/pages/FixPage.jsx`
   - `frontend/src/components/bugs/`
*Shared Frontend Files:* `frontend/src/services/api.js`, `frontend/src/App.jsx`.

---

## Setup & Running

### Backend Setup
1. Move to backend directory: `cd backend`
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create `.env` file from `.env.example` and set environment variables.
6. Run database migrations: `python -m database.init_db`
7. Start server: `uvicorn main:app --reload` (Runs on `http://localhost:8000`)

### Frontend Setup
1. Move to frontend directory: `cd frontend`
2. Install packages: `npm install`
3. Create `.env` file from `.env.example`
4. Run in dev mode: `npm run dev` (Runs on `http://localhost:5173`)
