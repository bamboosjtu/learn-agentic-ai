import os
import asyncio
from dotenv import load_dotenv, find_dotenv
from dataclasses import dataclass
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, RunContextWrapper

_: bool = load_dotenv(find_dotenv())

API_KEY: str | None = os.environ.get("AIHUBMIX_API_KEY")
BASE_URL: str | None = os.environ.get("AIHUBMIX_BASE_URL")

# Tracing disabled
set_tracing_disabled(disabled=True)

# 1. Which LLM Service?
external_client: AsyncOpenAI = AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL)

# 2. Which LLM Model?
llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model="gpt-4.1-mini-free", openai_client=external_client)

@dataclass
class UserContext:
    username: str
    email: str | None = None

@function_tool()
async def search(local_context: RunContextWrapper[UserContext], query: str) -> str:
    import time
    time.sleep(30)  # Simulating a delay for the search operation
    return "No other Math tutor found."

async def special_prompt(special_context: RunContextWrapper[UserContext], agent: Agent[UserContext]) -> str:
    # who is user?
    # which agent
    print(f"\nUser: {special_context.context},\nAgent: {agent.name}\n")
    return f"You are a good math tutor. User: {special_context.context.username}, Agent: {agent.name}. Please assist with math-related queries."

math_agent: Agent = Agent(name="Genius", instructions=special_prompt, model=llm_model, tools=[search])
# [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]

async def call_agent():
    # Call the agent with a specific input
    user_context = UserContext(username="abdullah")

    output = await Runner.run(
        starting_agent=math_agent, 
        input="search for the best math tutor in my area, include me",
        context=user_context
        )
    print(f"\n\nOutput: {output.final_output}\n\n")
    
asyncio.run(call_agent())