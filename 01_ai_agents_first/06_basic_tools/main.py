# 📦 Import Required Libraries
import os
from dotenv import load_dotenv

from agents import (
    Agent,                           # 🤖 Core agent class
    Runner,                          # 🏃 Runs the agent
    AsyncOpenAI,                     # 🌐 OpenAI-compatible async client
    OpenAIChatCompletionsModel,      # 🧠 Chat model interface
    function_tool,                   # 🛠️ Decorator to turn Python functions into tools
    set_default_openai_client,       # ⚙️ (Optional) Set default OpenAI client
    set_tracing_disabled,            # 🚫 Disable internal tracing/logging
)

# 🌿 Load environment variables from .env file
load_dotenv()



# 🚫 Disable tracing for clean output (optional for beginners)
set_tracing_disabled(disabled=True)

# 🔐 1) Environment & Client Setup
AIHUBMIX_API_KEY = os.getenv("AIHUBMIX_API_KEY")  # 🔑 Get your API key from environment
AIHUBMIX_BASE_URL = os.getenv("AIHUBMIX_BASE_URL")  # 🌐 Gemini-compatible base URL (set this in .env file)

# 🌐 Initialize the AsyncOpenAI-compatible client with Gemini details
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=AIHUBMIX_API_KEY,
    base_url=AIHUBMIX_BASE_URL,
)

# 🧠 2) Model Initialization
model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gpt-4o",        # ⚡ Fast Gemini model
    openai_client=external_client
)

# 🛠️ 3) Define tools (functions wrapped for tool calling)
@function_tool
def multiply(a: int, b: int) -> int:
    """🧮 Exact multiplication (use this instead of guessing math)."""
    return a * b

@function_tool
def sum(a: int, b: int) -> int:
    """➕ Exact addition (use this instead of guessing math)."""
    return a + b

# 🤖 4) Create agent and register tools
agent: Agent = Agent(
    name="Assistant",  # 🧑‍🏫 Agent's identity
    instructions=(
        "你是个超级助手，始终用中文答复。"
        "Always use tools for math questions. Always follow DMAS rule (division, multiplication, addition, subtraction). "
        "Explain answers clearly and briefly for beginners."
    ),
    model=model,
    tools=[multiply, sum],  # 🛠️ Register tools here
)

# 🧪 5) Run the agent with a prompt (tool calling expected)
prompt = "what is 19 + 23 * 2?"
result = Runner.run_sync(agent, prompt)

# 📤 Print the final result from the agent
print("\n🤖 CALLING AGENT\n")
print(result.final_output)
