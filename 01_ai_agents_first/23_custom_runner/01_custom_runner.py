import asyncio
import os

from dotenv import load_dotenv, find_dotenv

from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from agents.run import AgentRunner, set_default_agent_runner

_ = load_dotenv(find_dotenv())

API_KEY = os.getenv("AIHUBMIX_API_KEY")
BASE_URL = os.getenv("AIHUBMIX_BASE_URL")

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)

class CustomAgentRunner(AgentRunner):
    async def run(self, starting_agent, input, **kwargs):
        # Custom preprocessing
        print(f"CustomAgentRunner.run()")
        # input = await self.preprocess(input)
        
        # Call parent with custom logic
        result = await super().run(starting_agent, input, **kwargs)
        
        # Custom postprocessing & analytics
        # await self.log_analytics(result)
        return result

set_default_agent_runner(CustomAgentRunner())

set_tracing_disabled(disabled=True)

async def main():
    # This agent will use the custom LLM provider
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
        
    )

    result = await Runner.run(
        agent,
        "Tell me about recursion in programming.",
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
    

