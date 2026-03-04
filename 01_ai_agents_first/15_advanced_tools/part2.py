import os
import asyncio

from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, MaxTurnsExceeded

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
    return f"晴天"

base_agent: Agent = Agent(name="WeatherAgent", model=llm_model, tools=[get_weather])
print(base_agent.tools)

async def main():
    try:
        res = await Runner.run(base_agent, "What is weather in Lahore", max_turns=2)
        print(res.new_items)
    except MaxTurnsExceeded as e:
        print(f"Max turns exceeded: {e}")

if __name__ == "__main__":
    asyncio.run(main())