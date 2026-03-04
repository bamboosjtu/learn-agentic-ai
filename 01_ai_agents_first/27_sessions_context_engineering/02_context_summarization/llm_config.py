import os
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# SETUP FUNCTIONS
# ============================================================================

def setup_gemini_model():
    """Configure Gemini model using OpenAI-compatible API."""
    API_KEY = os.getenv("AIHUBMIX_API_KEY")
    BASE_URL = os.getenv("AIHUBMIX_BASE_URL")

    external_client = AsyncOpenAI(
        api_key=API_KEY,
        base_url=BASE_URL,
    )
    
    return OpenAIChatCompletionsModel(
        model="gpt-5-nano",
        openai_client=external_client
    )


# ============================================================================
# DEMO: CUSTOMER SUPPORT AGENT
# ============================================================================

# Create Gemini model
llm_model = setup_gemini_model()

# Create support agent
base_agent = Agent(
    name="Base Assistant",
    model=llm_model
)