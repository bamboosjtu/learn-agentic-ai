import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, SQLiteSession, OpenAIChatCompletionsModel, AsyncOpenAI

# 🌿 Load environment variables
load_dotenv(find_dotenv())

# 🔐 Setup Gemini client
API_KEY = os.getenv("AIHUBMIX_API_KEY")
BASE_URL = os.getenv("AIHUBMIX_BASE_URL")

external_client = AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL)
model = OpenAIChatCompletionsModel(model="gpt-5-nano", openai_client=external_client)

# Temporary memory (lost when program ends)
temp_session = SQLiteSession("temp_conversation")

# Persistent memory (saved to file)
persistent_session = SQLiteSession("user_123", "conversations.db")

agent = Agent(name="Assistant", instructions="You are helpful.", model=model)

# Use temporary session
result1 = Runner.run_sync(
    agent,
    "Remember: my favorite color is blue",
    session=temp_session
)

# Use persistent session
result2 = Runner.run_sync(
    agent,
    "Remember: my favorite color is blue",
    session=persistent_session
)

print("Both sessions now remember your favorite color!")
print("But only the persistent session will remember after restarting the program.")