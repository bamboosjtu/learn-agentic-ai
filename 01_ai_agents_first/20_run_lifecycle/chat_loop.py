import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, RunResult, set_tracing_disabled

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
    # handoffs=[news_agent]
)


user_chat: list[dict] = []
while True:
    user_input = input("Enter your input (or 'exit' to quit): ")
    if user_input.lower() == 'exit':
        break

    if user_input.lower() == 'view':
        print("\nCurrent Chat History:", user_chat)
    
    user_message = {"role": "user", "content": user_input}
    user_chat.append(user_message)
    
    res: RunResult = Runner.run_sync(starting_agent=base_agent, input=user_chat)
    
    user_chat = res.to_input_list()

    print("\nAGENT RESPONSE:", res.final_output)


# Now check the trace in
