from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth, project
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)

app = FastAPI(title="VentureLens AI")

app.include_router(auth.router)
app.include_router(project.router)

@app.get("/")
def root():
    return {"message": "VentureLens AI backend running"}
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)