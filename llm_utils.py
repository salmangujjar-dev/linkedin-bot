import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

load_dotenv()

def setup_llm():
    return AzureChatOpenAI(
        azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT"),
        api_version="2023-09-15-preview",
        temperature=0.3
    )