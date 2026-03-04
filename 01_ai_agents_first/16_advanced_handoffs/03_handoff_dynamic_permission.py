import asyncio
import os

from dotenv import load_dotenv, find_dotenv
from openai import AsyncOpenAI
from pydantic import BaseModel
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled, handoff

_ = load_dotenv(find_dotenv())

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

set_tracing_disabled(disabled=False)

class UserContext(BaseModel):
    user_id: str
    subscription_tier: str = "free"  # free, premium, enterprise
    has_permission: bool = False


# This agent will use the custom LLM provider
agent = Agent(
    name="Assistant",
    instructions="You only respond for the user's request and delegate to the expert agent if needed.",
    model=OpenAIChatCompletionsModel(model="gpt-5-nano", openai_client=external_client),
)

expert_agent = Agent(
    name="Expert",
    instructions="You are an expert in the field of recursion in programming.",
    model=OpenAIChatCompletionsModel(model="gpt-5-nano", openai_client=external_client),
)


agent.handoffs = [handoff(expert_agent, is_enabled=lambda ctx, agent: ctx.context.has_permission)]

async def main():
    context = UserContext(user_id="123", subscription_tier="premium", has_permission=False)

    result = await Runner.run(
        agent,
        "Call the expert agent and ask about recursion in programming",
        context=context,
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
    


