import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, RunContextWrapper, RunHooks, set_tracing_disabled

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
class HelloRunHooks(RunHooks):
        
    async def on_agent_start(self, context: RunContextWrapper, agent: Agent):
        print(f"\n\n[RunLifecycle] Agent {agent.name} start with context: {context}\n\n")
        
    async def on_llm_start(self, context: RunContextWrapper, agent: Agent, system_prompt, input_items):
        print(f"\n\n[RunLifecycle] LLM call for agent {agent.name} starting with system prompt: {system_prompt} and input items: {input_items}\n\n")
        
    
@function_tool
def get_weather(city: str) -> str:
    """A simple function to get the weather for a user."""
    return f"The weather for {city} is sunny."

news_agent: Agent = Agent(
    name="NewsAgent",
    instructions="You are a helpful news assistant.",
    model=llm_model,
)


base_agent: Agent = Agent(
    name="WeatherAgent",
    instructions="You are a helpful assistant. Talk about weather and let news_agent handle the news things",
    model=llm_model,
    tools=[get_weather],
    handoffs=[news_agent]
)

res = Runner.run_sync(
    starting_agent=base_agent, 
    input="What's the latest news about Qwen Code - seems like it can give though time to claude code.",
    hooks=HelloRunHooks()
    )

print(res.last_agent.name)
print(res.final_output)

# Now check the trace in 