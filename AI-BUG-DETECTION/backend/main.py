import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AI Bug Detection Tool API",
    description="Backend API for AI-powered Bug Detection and Auto-Remediation",
    version="1.0.0",
)

# Configure CORS
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
origins = [
    frontend_url,
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health endpoint
@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "service": "AI Bug Detection Backend"
    }

# Register Routers
from routes import analysis, bugs, fixes, validation, projects, dashboard

app.include_router(analysis.router, prefix="/api")
app.include_router(bugs.router, prefix="/api")
app.include_router(fixes.router, prefix="/api")
app.include_router(validation.router, prefix="/api")
app.include_router(projects.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
