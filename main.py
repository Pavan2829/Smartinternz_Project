from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .engine import SmartinternzEngine
import os

app = FastAPI(title="Smartinternz_Project API")

# Allow the frontend HTML to talk to this Python backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = SmartinternzEngine()

class QueryRequest(BaseModel):
    question: str

@app.on_event("startup")
async def startup_event():
    # Automatically build the database from your text file on start
    engine.build_index("data/agri_knowledge.txt")

@app.post("/ask")
async def ask_farmer_query(request: QueryRequest):
    answer = engine.query(request.question)
    return {"answer": answer}
