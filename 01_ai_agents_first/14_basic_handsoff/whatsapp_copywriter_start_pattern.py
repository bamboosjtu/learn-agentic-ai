#  0. Importing the necessary libraries
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, function_tool

import os
from dotenv import load_dotenv, find_dotenv

# 0.1. Loading the environment variables
load_dotenv(find_dotenv())

API_KEY = os.environ.get("AIHUBMIX_API_KEY")
BASE_URL = os.environ.get("AIHUBMIX_BASE_URL")


# 1. Which LLM Provider to use? -> Google Chat Completions API Service
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)

# 2. Which LLM Model to use?
llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gpt-5-nano",
    openai_client=external_client
)

@function_tool
def get_unread_whatsapp_messages() -> str:
    """Check and returns unread WhatsApp messages and share them."""
    # Simulated unread messages
    return "You have 1 unread messages: 'Create a promotional copy for our new sneakers launch!'"

# Pattern: Agent as tool
whatsapp_monitor: Agent = Agent(
    name="WhatsApp Monitor", 
    instructions="""Check unread WhatsApp messages and delegate when intent indicates.
    Use tools for whatsapp interaction. Do not assume anything.
    """,
    model=llm_model, 
    tools=[get_unread_whatsapp_messages],
    handoff_description="Check WhatsApp messages."
    )

copywriter: Agent = Agent(name="Copywriter",
                          instructions="""Create promotional copies based on WhatsApp message requests.""",
                          model=llm_model, handoffs=[whatsapp_monitor],
                          handoff_description="Handles requests for promotional copywriting."
                          )

whatsapp_monitor.handoffs = [copywriter]

# 4. Running the Agent
result = Runner.run_sync(starting_agent=copywriter, 
                         input="""Check the WhatsApp messages and create promotional copies as needed.""",
                         )

print("\nACTIVE AGENT: " , result.last_agent.name)
print("\nAGENT RESPONSE: " , result.final_output)
