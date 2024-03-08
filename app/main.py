import os
import re
import requests
import asyncio
import aiohttp
from openai import OpenAI
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from app.repositories.langchain_repository import LangChainRepository
# from app.repositories.scrapbox_repository import ScrapboxRepository

load_dotenv()

langchain_repository = LangChainRepository(client=OpenAI(api_key=os.getenv("OPENAI_API_KEY")))
# scrapbox_repository = ScrapboxRepository(os.getenv("SCRAPBOX_PROJECT_NAME"))

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

question_pattarn = re.compile(r"\?")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/webhook")
async def line_webhook(request: Request):
    body = await request.json()
    signature = request.headers["X-Line-Signature"]
    try:
        handler.handle(body.decode(), signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        return "NG", 400

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    question = event.message.text
    answer = langchain_repository.generate_gpt_answer(question)
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=answer["content"])
    )

connector = aiohttp.TCPConnector(ssl=False)
deploy_url = "https://christian-6ibjha4nnq-an.a.run.app"
async def send_request():
    while True:
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(deploy_url) as response:
                print(await response.text())
        await asyncio.sleep(30)  # 50秒ごとにリクエストを送信


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(send_request())
