import os
import asyncio
from dotenv import load_dotenv, find_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, set_default_openai_api, set_default_openai_client,set_tracing_export_api_key

from openinference.instrumentation.openai_agents import OpenAIAgentsInstrumentor
from langfuse import get_client


# -----------------------------
# Load environment and configure
# -----------------------------
load_dotenv(find_dotenv())  # Load local .env file

# Instrumentation setup
OpenAIAgentsInstrumentor().instrument()

# Load environment variables
os.getenv("LANGFUSE_PUBLIC_KEY")
os.getenv("LANGFUSE_SECRET_KEY")
os.getenv("LANGFUSE_HOST")

# Set OpenAI API key
API_KEY = os.getenv("AIHUBMIX_API_KEY")
BASE_URL = os.getenv("AIHUBMIX_BASE_URL")


client = AsyncOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

set_default_openai_client(client=client, use_for_tracing=False)
set_default_openai_api("chat_completions")

# -----------------------------
# Initialize Langfuse client
# -----------------------------
langfuse = get_client()

# Verify connection
if langfuse.auth_check():
    print("✅ Langfuse client is authenticated and ready!")
else:
    print("❌ Authentication failed. Please check your credentials and host.")


# -----------------------------
# Define async main function
# -----------------------------
async def main():
    """Run an AI agent that replies in haikus."""
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model = "gpt-5-nano",
    )

    result = await Runner.run(agent, "Tell me about recursion in programming.")
    print("\n--- Agent Response ---")
    print(result.final_output)


# -----------------------------
# Entry point
# -----------------------------
if __name__ == "__main__":
    asyncio.run(main())
