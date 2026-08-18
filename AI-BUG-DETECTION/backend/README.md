# AI Bug Detection Backend

This is the FastAPI backend for the AI Bug Detection and Auto-Remediation platform.

## Structure & Responsibilities

- `routes/`: Expresses API routes, handles request parsing and delegates business logic to services.
- `services/`: Contains the core logic.
  - Disha owns: `ai_analyzer.py`, `bug_classifier.py`, `severity_engine.py`, `fix_generator.py`, `prompt_manager.py`.
  - Pavan owns: `static_analyzer.py`, `result_fusion.py`, `validation_service.py`.
- `models/`: Database models.
- `schemas/`: Pydantic request/response validation schemas.
- `database/`: DB connection & initialization.
- `utils/`: Common utilities (e.g. logging, syntax parsing).
- `prompts/`: Raw text files defining prompt structures for the AI engines.

## Getting Started

1. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Or `venv\Scripts\activate` on Windows
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize the database:
   ```bash
   python -m database.init_db
   ```
4. Start the application:
   ```bash
   uvicorn main:app --reload
   ```
