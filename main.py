from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
import openai
import os

app = FastAPI()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("1f327eb4cab7b572bdd86d49949b0ad3127fea66e84427d1bb30a014b48aaf58")
ONLINEPBX_API_KEY = os.getenv("ONLINEPBX_API_KEY")
ONLINEPBX_SIP_DOMAIN = os.getenv("ONLINEPBX_SIP_DOMAIN")
CALL_FROM_NUMBER = os.getenv("CALL_FROM_NUMBER")

openai.api_key = OPENAI_API_KEY

class CallRequest(BaseModel):
    phone_number: str

@app.post("/call")
async def initiate_call(data: CallRequest):
    payload = {
        "from": CALL_FROM_NUMBER,
        "to": data.phone_number,
        "sip_domain": ONLINEPBX_SIP_DOMAIN
    }
    headers = {
        "Authorization": f"Bearer {ONLINEPBX_API_KEY}"
    }
    response = requests.post("https://app.onlinepbx.ru/api/calls/", json=payload, headers=headers)
    return {"status": "call started", "response": response.json()}

@app.post("/webhook")
async def onlinepbx_webhook(req: Request):
    data = await req.json()
    print("Webhook получен:", data)
    return {"ok": True}

@app.post("/generate-reply")
async def generate_reply(req: Request):
    body = await req.json()
    message = body.get("message")
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ты голосовой помощник, общаешься с клиентом дружелюбно и уверенно."},
            {"role": "user", "content": message}
        ]
    )
    return {"response": response.choices[0].message.content}

@app.get("/")
def root():
    return {"message": "Voicebot работает"}
