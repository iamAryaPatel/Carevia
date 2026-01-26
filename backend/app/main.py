from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.job_routes import router as job_router
from app.scheduler import start_scheduler

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(job_router)

# Start scheduler
start_scheduler()

@app.get("/")
def root():
    return {"message": "Carevia backend running"}
