from fastapi import FastAPI

from app.auth.routes import router as auth_router
from app.health.routes import router as health_router


app = FastAPI(title="HealthOS")


app.include_router(auth_router)
app.include_router(health_router)


@app.get("/")
def root():
    return {"message": "HealthOS API is running"}