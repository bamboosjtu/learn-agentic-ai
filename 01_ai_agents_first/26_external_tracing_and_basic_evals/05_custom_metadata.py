import os
import asyncio
from dotenv import load_dotenv, find_dotenv
from openai import AsyncOpenAI
from openinference.instrumentation.openai_agents import OpenAIAgentsInstrumentor
from langfuse import get_client, observe
from agents import Agent, Runner, set_default_openai_api, set_default_openai_client, set_tracing_export_api_key


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
# --- Environment setup
API_KEY = os.getenv("AIHUBMIX_API_KEY")
BASE_URL = os.getenv("AIHUBMIX_BASE_URL")

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

set_default_openai_client(client=client, use_for_tracing=False)
set_default_openai_api("chat_completions")
set_tracing_export_api_key(API_KEY)

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
# Define async main function with @observe decorator
# -----------------------------
@observe()
async def main():
    """Run an AI agent that replies in haikus."""
    input_text = "Tell me about recursion in programming."

    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model="gpt-5-nano",
    )

    result = await Runner.run(agent, input_text)
    output = result.final_output

    # Add metadata to the span
    langfuse.update_current_span(
        input=input_text,
        output=output,
        metadata={
            "model": "gpt-5-nano",
            "agent_type": "haiku_generator",
            "topic": "recursion",
            "user_id": "user_gemini_001",
            "session_id": "session_haiku_demo",
            "tags": ["agent", "haiku", "gemini", "recursion"],
            "version": "1.0.0"
        }
    )
    
    print("\n--- Agent Response ---")
    print(output)
    
    return output


# -----------------------------
# Entry point
# -----------------------------
if __name__ == "__main__":
    asyncio.run(main())
    
    # Flush events to ensure they're sent to Langfuse
    langfuse.flush()