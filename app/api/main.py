from fastapi import FastAPI

from app.api.routes.jobs import router as jobs_router

app = FastAPI(
    title="AI Recruitment Platform",
    version="1.0.0",
)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "ai-recruitment-platform",
    }
app.include_router(jobs_router)