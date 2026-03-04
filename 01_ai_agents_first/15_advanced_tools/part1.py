import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, StopAtTools

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
    """A simple function to get the weather for a user."""
    return f"晴天"

@function_tool
def get_travel_plan(city: str) -> str:
    """Plan Travel for your city"""
    return f"旅行行程规划不可用。"


base_agent: Agent = Agent(
    name="WeatherAgent",
    instructions="你是一个超级助手，只说中文。",
    model=llm_model,
    tools=[get_weather, get_travel_plan],
    tool_use_behavior=StopAtTools(stop_at_tool_names=["get_travel_plan"])
)

# res = Runner.run_sync(base_agent, "What is weather in Lahore")
res = Runner.run_sync(base_agent, "Make me travel plan for Lahore")
print(res.final_output)

# 1. NLP answer = loop finished
# 2. tool call = loop continue - loop finish

# tool call = ASK Question from Human = loop pause
