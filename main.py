from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import openai
import os

app = FastAPI()

# Подключаем CORS — разрешаем запросы с любых доменов (можно сузить до домена Тильды)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # или ["http://smm3.it-resheniya.com/irobot", "http://smm3.it-resheniya.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Читаем ключи из переменных окружения
OPENAI_API_KEY = os.getenv("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")
ELEVENLABS_API_KEY = os.getenv("1f327eb4cab7b572bdd86d49949b0ad3127fea66e84427d1bb30a014b48aaf58")
ONLINEPBX_API_KEY = os.getenv("QVA2ZVhHcmExbENRcHlyMjBmUEY3NWo5elpNNFhFOUo")
ONLINEPBX_SIP_DOMAIN = os.getenv("pbx26432.onpbx.ru")
CALL_FROM_NUMBER = os.getenv("79011477868")

openai.api_key = OPENAI_API_KEY

class CallRequest(BaseModel):
    phone_number: str

@app.get("/")
def root():
    return {"message": "Voicebot работает"}

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

@app.post("/generate-reply")
async def generate_reply(req: Request):
    body = await req.json()
    message = body.get("message")
    response = openai.ChatCompletion.create(
        model="gpt‑4",
        messages=[
            {"role": "system", "content": "Ты голосовой помощник, общаешься с клиентом дружелюбно и уверенно."},
            {"role": "user", "content": message}
        ]
    )
    answer = response.choices[0].message.content
    return {"response": answer}
