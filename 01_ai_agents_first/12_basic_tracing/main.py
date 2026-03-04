import os
import asyncio
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, trace, set_trace_processors
from agents.tracing.processors import BatchTraceProcessor, ConsoleSpanExporter

_: bool = load_dotenv(find_dotenv())

# 用“只打印控制台”的处理器替换默认处理器
set_trace_processors([
    BatchTraceProcessor(ConsoleSpanExporter())
])

API_KEY = os.environ.get("AIHUBMIX_API_KEY")
BASE_URL = os.environ.get("AIHUBMIX_BASE_URL")

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


# Now check the trace in 

async def main():
    agent = Agent(name="Joke generator", instructions="Tell funny jokes about linabell in Chiesee.", model=llm_model)

    with trace("Joke workflow"): 
        first_result = await Runner.run(agent, "Tell me a joke")
        second_result = await Runner.run(agent, f"Rate this joke: {first_result.final_output}")
        print(f"Joke: {first_result.final_output}")
        print(f"Rating: {second_result.final_output}")
    print("Run finished. If timeout logs appear below, the model call succeeded and only trace export failed.")

asyncio.run(main())
