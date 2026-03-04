import os
from dotenv import load_dotenv
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig

# Load the environment variables from the .env file
load_dotenv()

API_KEY = os.getenv("AIHUBMIX_API_KEY")
BASE_URL = os.getenv("AIHUBMIX_BASE_URL")



#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)

model = OpenAIChatCompletionsModel(
    model="gpt-5-nano",
    openai_client=external_client
)

google_gemini_config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)