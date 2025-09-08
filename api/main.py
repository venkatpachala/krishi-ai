from fastapi import FastAPI
from .db import init_db
from .routers import ask, escalate, feedback

app = FastAPI(title="Krishi AI")

app.include_router(ask.router)
app.include_router(escalate.router)
app.include_router(feedback.router)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def read_root():
    return {"status": "ok"}
