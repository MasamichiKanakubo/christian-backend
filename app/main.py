import os
import json
import re
import requests
import logging
import asyncio
import aiohttp
from openai import OpenAI
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from app.repositories.langchain_repository import LangChainRepository

# from app.repositories.scrapbox_repository import ScrapboxRepository

load_dotenv()

langchain_repository = LangChainRepository(
    client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
)
# scrapbox_repository = ScrapboxRepository(os.getenv("SCRAPBOX_PROJECT_NAME"))

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

url = 'https://scrapbox.io/api/pages/christian-beginners/'

question_re_pattern = re.compile(r"\?")

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


@app.post("/")
async def callback(request: Request, background_tasks: BackgroundTasks):
    body = await request.body()
    data_json = json.loads(body)
    
    if data_json["events"]:
        try:
            background_tasks.add_task(handle_message, data_json)
        except IndexError:
            return {"error": "Invalid event data"}
    else:
        return {"error": "Events not found"}
    return {"message": "OK"}

@handler.add(MessageEvent)
def handle_message(data_json):
    incoming_text = data_json["events"][0]["message"]["text"]
    reply_token = data_json["events"][0]["replyToken"]
    
    with open("app/use_cases/scrapbox/faqs.json", "r", encoding="utf-8") as file:
        faqs = json.load(file)
        
    for item in faqs:
        if incoming_text in item:
            response = requests.get(url + item[incoming_text]).json()
            descriptions = response.get("descriptions", [])
            
            descriptions_list: list = [
                description for description in descriptions
                if not question_re_pattern.search(description)
            ]
            description_text = "".join(descriptions_list)
            reply_message = TextSendMessage(text=description_text)
            line_bot_api.reply_message(reply_token, reply_message)
            return
    
    default_text = TextSendMessage(text="質問に対する回答は見つかりませんでした。")
    line_bot_api.reply_message(reply_token, default_text)
            

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
