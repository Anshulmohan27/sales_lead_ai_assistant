from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main import client, get_lead_info, get_lead_info_by_company, search_product_docs
from google.genai import errors

app = FastAPI(
    title="Sales Lead AI Assistant",
    description="An AI agent that answers questions about leads (CRM) and product info (RAG) using Gemini.",
    version="1.0.0"
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat", response_model=ChatResponse, summary="Ask the sales assistant a question"))
def chat(request: ChatRequest):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=request.message,
            config={'tools': [get_lead_info, get_lead_info_by_company, search_product_docs]}
        )
        return {"reply": response.text}
    except errors.ClientError:
        raise HTTPException(status_code=429, detail="Rate limited — please try again shortly.")