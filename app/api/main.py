from fastapi import FastAPI

from app.api.routes.jobs import router as jobs_router
from app.api.routes.resume import router as resume_router


app = FastAPI(
    title="AI Recruitment Platform",
    version="1.0.0",
)


# Register Jobs API
app.include_router(jobs_router)

# Register Resume API
app.include_router(resume_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "ai-recruitment-platform",
    }