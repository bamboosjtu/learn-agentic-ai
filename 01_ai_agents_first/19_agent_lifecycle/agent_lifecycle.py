import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, AgentHooks, RunContextWrapper, set_tracing_disabled

_: bool = load_dotenv(find_dotenv())
set_tracing_disabled(True)

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


# Agent Lifecycle Callbacks/Hooks
class HelloAgentHooks(AgentHooks):
    def __init__(self, lifecycle_name: str):
        self.lifecycle_name = lifecycle_name
        
    async def on_start(self, context, agent):
        context.context
        print(f"\n\n[{self.lifecycle_name}] Agent {agent.name} starting with context: {context}\n\n")
        
    async def on_llm_start(self, context: RunContextWrapper, agent, system_prompt, input_items):
        print(f"\n\n[{self.lifecycle_name}] LLM call starting with system prompt: {system_prompt} and input items: {input_items}\n\n")
        
    async def on_llm_end(self, context, agent, response):
        print(f"\n\n[{self.lifecycle_name}] LLM call ended with response: {response}\n\n")
        
    async def on_end(self, context, agent, output):
        print(f"\n\n[{self.lifecycle_name}] Agent {agent.name} ended with output: {output}\n\n")


@function_tool
def get_weather(city: str) -> str:
    """A simple function to get the weather for a user."""
    return f"The weather for {city} is sunny."



news_agent: Agent = Agent(
    name="NewsAgent",
    instructions="You are a helpful news assistant.",
    model=llm_model,
    hooks=HelloAgentHooks("NewsAgentLifecycle")
)


base_agent: Agent = Agent(
    name="WeatherAgent",
    instructions="You are a helpful assistant. Talk about weather and let news_agent handle the news things",
    model=llm_model,
    tools=[get_weather],
    hooks=HelloAgentHooks("WeatherAgentLifecycle"),
    handoffs=[news_agent]
)

res = Runner.run_sync(base_agent, "What's the latest news about Qwen Code - seems like it can give though time to claude code.")
print(res.last_agent.name)
print(res.final_output)

# Now check the trace in 