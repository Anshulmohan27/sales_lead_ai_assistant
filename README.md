# Sales Lead AI Assistant

An AI assistant that helps sales reps get answers instantly — whether they're asking about a specific lead's status or a question about product pricing and features. Built to explore how LLM agents can combine **structured data lookup** (CRM records) with **unstructured knowledge retrieval** (RAG over product docs) in a single conversational interface.

**Live demo:** [sales-lead-ai-assistant.onrender.com/docs](https://sales-lead-ai-assistant.onrender.com/docs) — try the `/chat` endpoint directly (note: free-tier hosting spins down after inactivity, so the first request may take 30-60 seconds to wake up)

## Why I built this

Coming from a marketing/sales background, I've seen firsthand how much time reps lose context-switching between a CRM and internal docs just to answer simple questions. This project is a small proof-of-concept of an assistant that removes that friction — and a hands-on way for me to learn the core building blocks of modern AI engineering: LLM APIs, tool use, and retrieval-augmented generation.

## How it works

The assistant is given two tools and decides on its own which one (if any) a question needs:

1. **`get_lead_info`** — looks up a lead's company, deal value, stage, and notes from a CRM object, given a client's name
2. **`search_product_docs`** — performs semantic search over a small vector database of product documentation (pricing, features, policies) and returns the most relevant context

The LLM (Gemini 2.5 Flash) reads the user's question, calls the appropriate tool automatically via function calling, and generates a natural-language answer grounded in the real data returned — rather than guessing.

## Tech stack

- **Google Gemini API** (`google-genai`) — LLM calls, function calling, embeddings
- **ChromaDB** — local vector database for semantic search over product docs
- **FastAPI** — REST API layer exposing the assistant as a `POST /chat` endpoint
- **python-dotenv** — safe API key management

## API

The assistant is exposed as a FastAPI web service (`api.py`), separate from the core logic (`main.py`) — following a clean separation between business logic and the web layer.

**Endpoint:** `POST /chat`
**Request body:** `{"message": "What's the status on the Jensen deal?"}`
**Response:** `{"reply": "The Jensen deal with NVIDIA is currently in the negotiation stage..."}`

Includes graceful handling of API rate limits (returns a clean `429` instead of a raw crash) and Pydantic request validation.

Run it with:
```bash
uvicorn api:app --reload
```
Then visit `http://127.0.0.1:8000/docs` for an interactive testing UI.

## Example interaction

```
You: What's the status on the Jensen deal?
Assistant: The Jensen deal with NVIDIA is currently in the negotiation stage,
with a deal value of $50,000. They are interested in more features.

You: What's included in the enterprise plan?
Assistant: Our Enterprise plan costs $499/month and includes unlimited users
and priority support. Enterprise customers also get a dedicated account
manager and custom onboarding.

You: What's the weather today?
Assistant: I can only access information about client leads and product
documentation. I cannot tell you the weather.
```

Note the third example: the assistant correctly declines to answer when neither tool applies, rather than hallucinating a response.

## Running it locally

```bash
git clone https://github.com/Anshulmohan27/sales_lead_ai_assistant.git
cd sales_lead_ai_assistant
python -m venv myenv
myenv\Scripts\activate      # Windows
pip install -r requirements.txt
```

Create a `.env` file in the project root:
```
GEMINI_API_KEY=your-key-here
```

Get a free key at [aistudio.google.com](https://aistudio.google.com) (no credit card required).

Then run:
```bash
python main.py
```

## What I'd build next

- Move the CRM from in-memory Python objects to a real database (SQLite/PostgreSQL)
- Wrap this in a FastAPI backend so it's a real web service, not just a CLI
- Add conversation memory so follow-up questions retain context
- Deploy it with a simple web front-end

## About me

Transitioning from a marketing/sales background into AI engineering. This project is part of my learning journey building practical, product-minded AI applications.
