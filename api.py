from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main import chat_with_memory
from google.genai import errors
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(
    title="Sales Lead AI Assistant",
    description="An AI agent that answers questions about leads (CRM) and product info (RAG) using Gemini.",
    version="1.0.0"
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat", summary="Ask the sales assistant a question")
def chat(request: ChatRequest):
    try:
        answer = chat_with_memory(request.message)
        return {"reply": answer}
    except errors.ClientError:
        raise HTTPException(status_code=429, detail="Rate limited — please try again shortly.")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_ui():
    return FileResponse("static/index.html")