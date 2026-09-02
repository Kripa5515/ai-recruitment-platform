from fastapi import FastAPI
from app.api.schemas.job import JobCreate

app = FastAPI(
    title="AI Recruitment Platform",
    version="1.0.0",
)

@app.get("/health")
def health_check():
    return {
        "status" : "ok",
        "service": "ai-recruitment-platform",
    }

@app.post("/jobs")
def create_job(job: JobCreate):
    return {
        "message": "Job received successfully",
        "job": job,
    }
