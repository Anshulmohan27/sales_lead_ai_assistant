from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main import client, get_lead_info, get_lead_info_by_company, search_product_docs
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

conversation_history = []

@app.post("/chat", summary="Ask the sales assistant a question")
def chat(request: ChatRequest):
    conversation_history.append({"role": "user", "parts": [{"text": request.message}]})
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=conversation_history,
            config={'tools': [get_lead_info, get_lead_info_by_company, search_product_docs]}
        )
        conversation_history.append({"role": "model", "parts": [{"text": response.text}]})
        return {"reply": response.text}
    except errors.ClientError:
        raise HTTPException(status_code=429, detail="Rate limited — please try again shortly.")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_ui():
    return FileResponse("static/index.html")