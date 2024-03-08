import os
import re
import requests
import asyncio
import aiohttp
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

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


connector = aiohttp.TCPConnector(ssl=False)
deploy_url = "http://localhost:8080"
async def send_request():
    while True:
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(deploy_url) as response:
                print(await response.text())
        await asyncio.sleep(50)  # 50秒ごとにリクエストを送信


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(send_request())
