from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.agent import CognitiveAgent


app = FastAPI(
    title="Intelligent Cognitive Assistant API",
    description="AI-powered cognitive assistant using Llama 3.2",
    version="1.0"
)


# -----------------------------------
# CORS
# -----------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------
# AI AGENT
# -----------------------------------

agent = CognitiveAgent()


# -----------------------------------
# REQUEST MODEL
# -----------------------------------

class ChatRequest(BaseModel):
    message: str


# -----------------------------------
# WEBSITE
# -----------------------------------

@app.get("/")
def home():

    return FileResponse("app/frontend/index.html")


# -----------------------------------
# CHAT API
# -----------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    result = agent.process(request.message)

    return {
        "intent": result["intent"],
        "response": result["response"]
    }