import os
import asyncio

from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
from agents import set_tracing_disabled

set_tracing_disabled(True)

_: bool = load_dotenv(find_dotenv())

# ONLY FOR TRACING
API_KEY = os.environ.get("AIHUBMIX_API_KEY", "")
BASE_URL = os.environ.get("AIHUBMIX_BASE_URL", "")

# 1. Which LLM Service?
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)

# 2. Which LLM Model?
llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gpt-5-nano",
    openai_client=external_client
)

@function_tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    try:
        print(f"[TOOL] get_weather called with city={city}")
        return f"The current weather in {city} is sunny."
    except ValueError:
        raise ValueError("Weather service is currently unavailable.")
    except TimeoutError:
        raise TimeoutError("Weather service request timed out.")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {str(e)}")

base_agent: Agent = Agent(
    name="WeatherAgent",
    instructions=(
        "You are a weather assistant. "
        "If the user asks about weather, you must call the get_weather tool. "
        "Do not answer from memory."
    ),
    model=llm_model,
    tools=[get_weather],
)

async def main():
    res = await Runner.run(base_agent, "What is weather in Lahore")
    print(res.new_items)
    print(res.final_output)

if __name__ == "__main__":
    asyncio.run(main())
