import pandas as pd
import chromadb
from langchain import llms
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.indexes import VectorstoreIndexCreator
from datasets import load_dataset
from langchain_community.document_loaders import TextLoader
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

loader = TextLoader("app/data/questions.txt", encoding="utf-8")
documents = loader.load()

vectordb = Chroma.from_documents(
    documents=documents,
    embedding=OpenAIEmbeddings(api_key=openai_api_key),
    persist_directory="app/vectorstore"
)
if vectordb:
    print(vectordb)
    vectordb.persist()
    vectordb = None
else:
    print("Chroma DB has not been initialized.")
