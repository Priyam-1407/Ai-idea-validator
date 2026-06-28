from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="VentureLens AI")

app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "VentureLens AI backend running"}