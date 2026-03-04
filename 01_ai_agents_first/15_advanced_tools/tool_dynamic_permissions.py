import asyncio
import os

from dotenv import load_dotenv, find_dotenv
from openai import AsyncOpenAI
from pydantic import BaseModel
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled, RunContextWrapper, function_tool

_ = load_dotenv(find_dotenv())

API_KEY = os.environ.get("AIHUBMIX_API_KEY", "")
BASE_URL = os.environ.get("AIHUBMIX_BASE_URL", "")

#Reference: https://ai.google.dev/gemini-api/docs/openai
client = AsyncOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)

set_tracing_disabled(disabled=False)

class UserContext(BaseModel):
    user_id: str
    subscription_tier: str = "free"  # free, premium, enterprise
    has_permission: bool = False


def premium_feature_enabled(context: RunContextWrapper, agent: Agent) -> bool:
    print(f"premium_feature_enabled()")
    print(context.context.subscription_tier, context.context.subscription_tier in ["premium", "enterprise"])
    return context.context.subscription_tier in ["premium", "enterprise"]

@function_tool(is_enabled=premium_feature_enabled)
def get_weather(city: str) -> str:
    print(f"[ADV] get_weather()")
    return "天气是晴天。"

# This agent will use the custom LLM provider
agent = Agent(
    name="Assistant",
    instructions="You only respond in Chinese.You must call the get_weather tool whenever the user asks about weather.",
    model=OpenAIChatCompletionsModel(model="gpt-5-nano", openai_client=client),
    tools=[get_weather]
)

async def main():
    context = UserContext(user_id="123", subscription_tier="premium", has_permission=True)
    # context = UserContext(user_id="123", subscription_tier="basic", has_permission=True)

    result = await Runner.run(
        agent,
        "Call the get_weather tool with city 'London'",
        context=context,
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
    


