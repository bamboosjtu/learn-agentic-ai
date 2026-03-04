import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, SQLiteSession, OpenAIChatCompletionsModel, AsyncOpenAI

# 🌿 Load environment variables
load_dotenv(find_dotenv())

# 🔐 Setup Gemini client
API_KEY = os.getenv("AIHUBMIX_API_KEY")
BASE_URL = os.getenv("AIHUBMIX_BASE_URL")

external_client = AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL)
llm_model = OpenAIChatCompletionsModel(model="gpt-5-nano", openai_client=external_client)

# Create agent
agent = Agent(
    name="Assistant",
    instructions="作为一个个人助手，说话要得体友善。",
    model=llm_model,
)

# Create session memory
session = SQLiteSession("my_first_conversation")

print("=== First Conversation with Memory ===")

# Turn 1
result1 = Runner.run_sync(
    agent,
    "你好，我叫袋鼠，我喜欢吃达美乐。",
    session=session,
)
print("Agent:", result1.final_output)

# Turn 2 - Agent should remember your name!
result2 = Runner.run_sync(
    agent,
    "我是谁?",
    session=session
)
print("Agent:", result2.final_output)  # Should say "Alex"!

# Turn 3 - Agent should remember you love pizza!
result3 = Runner.run_sync(
    agent,
    "我喜欢吃啥。",
    session=session
)

print("Agent:", result3.final_output)  # Should say "Alex"!

print("\n\nNO SESSION MEMORY\n\n")
result4 = Runner.run_sync(
    agent,
    "我是谁，我喜欢的食物?"
)
print("Agent:", result4.final_output)  # Should mention pizza!