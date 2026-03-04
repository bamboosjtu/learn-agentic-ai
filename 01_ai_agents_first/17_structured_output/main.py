import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, ModelSettings, function_tool

# 🌿 Load environment variables
load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.environ.get("AIHUBMIX_API_KEY", "")
BASE_URL = os.environ.get("AIHUBMIX_BASE_URL", "")

external_client = AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL)
llm_model = OpenAIChatCompletionsModel(model="gpt-5-nano", openai_client=external_client)


from pydantic import BaseModel
from agents import Agent, Runner

# Define your data structure
class PersonInfo(BaseModel):
    name: str
    age: int
    occupation: str

# Create agent with structured output
agent = Agent(
    name="InfoCollector",
    model=llm_model,
    instructions="从用户消息中提取个人信息。",
    output_type=PersonInfo  # This is the magic!
)

async def main():
    result = await Runner.run(
        agent,
        "你好, 我叫袋鼠, 今年二十五岁，职业是一名老师。"
    )

    # Now you get perfect structured data!
    print("Type:", type(result.final_output))        # <class 'PersonInfo'>
    print("Name:", result.final_output.name)         # "Alice"
    print("Age:", result.final_output.age)           # 25
    print("Job:", result.final_output.occupation)    # "teacher"


if __name__ == "__main__":
    asyncio.run(main())
