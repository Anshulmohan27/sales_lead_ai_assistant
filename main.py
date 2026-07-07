import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import errors
import chromadb

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


class Deal:
    def __init__(self, client_name: str, company: str, deal_value: int, stage: str, notes: str):
        self.client_name = client_name
        self.company = company
        self.deal_value = deal_value
        self.stage = stage
        self.notes = notes


class CRM:
    def __init__(self):
        self.deals = []

    def add_deal(self, deal: Deal):
        self.deals.append(deal)

    def get_lead_info(self, client_name: str) -> dict:
        for deal in self.deals:
            if deal.client_name == client_name:
                return {"company": deal.company, "deal_value": deal.deal_value,
                        "stage": deal.stage, "notes": deal.notes}
        return {"error": f"No lead found for {client_name}"}

    def get_lead_info_by_company(self, company: str) -> dict:
        for deal in self.deals:
            if deal.company == company:
                return {"client_name": deal.client_name, "deal_value": deal.deal_value,
                        "stage": deal.stage, "notes": deal.notes}
        return {"error": f"No lead found for {company}"}


amex = Deal('John', 'Amex', 5000, 'negotiation', 'want to go lower')
apple = Deal('Stuart', 'Apple', 40000, 'prospecting', 'not sure if Stuart is the right person')
nvidia = Deal('Jensen', 'NVIDIA', 50000, 'negotiation', 'Want more features')
tesla = Deal('Elon', 'Tesla', 9000, 'closed', 'one year contract')

crm = CRM()
crm.add_deal(amex)
crm.add_deal(apple)
crm.add_deal(nvidia)
crm.add_deal(tesla)

chroma_client = chromadb.Client()
product_kb = chroma_client.create_collection(name="product_kb")
product_kb.add(
    documents=[
        "Our Enterprise plan costs $499/month and includes unlimited users and priority support.",
        "Our Starter plan costs $49/month and supports up to 5 users.",
        "We offer a 30-day money-back guarantee on all plans.",
        "Enterprise customers get a dedicated account manager and custom onboarding.",
    ],
    ids=["doc1", "doc2", "doc3", "doc4"]
)


def get_lead_info(client_name: str) -> dict:
    """Look up CRM info (company, deal value, stage, notes) for a given client name.
    client_name is a first name, e.g. 'Jensen', 'Elon', 'John', 'Stuart'."""
    return crm.get_lead_info(client_name)


def get_lead_info_by_company(company: str) -> dict:
    """Look up CRM info (client name, deal value, stage, notes) for a given company.
    company is the name of a company, e.g. 'NVIDIA', 'Tesla', 'Amex', 'Apple'."""
    return crm.get_lead_info_by_company(company)


def search_product_docs(question: str) -> str:
    """Search product knowledge base (pricing, features, policies) for relevant info."""
    results = product_kb.query(query_texts=[question], n_results=2)
    return "\n".join(results["documents"][0])

conversation_history = []

def chat_with_memory(user_message: str) -> str:
    conversation_history.append({"role": "user", "parts": [{"text": user_message}]})
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=conversation_history,
        config={'tools': [get_lead_info, get_lead_info_by_company, search_product_docs]}
    )
    
    conversation_history.append({"role": "model", "parts": [{"text": response.text}]})
    return response.text

if __name__ == "__main__":
    print("Sales Assistant ready. Type 'quit' to exit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        try:
            answer = chat_with_memory(user_input)

            print(f"Assistant: {answer}\n")
        except errors.ClientError:
            print("Assistant: I'm getting rate-limited right now — please wait a moment and try again.\n")