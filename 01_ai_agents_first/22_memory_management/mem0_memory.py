import os
from dataclasses import dataclass

from dotenv import load_dotenv, find_dotenv
from agents import (
    Agent,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    RunContextWrapper,
    Runner,
    function_tool,
    set_tracing_disabled,
)
from agents.tool_context import ToolContext
from mem0 import MemoryClient


@dataclass
class UserContext:
    username: str


_: bool = load_dotenv(find_dotenv())

set_tracing_disabled(True)

API_KEY = os.getenv("AIHUBMIX_API_KEY")
BASE_URL = os.getenv("AIHUBMIX_BASE_URL")
MEM0_API_KEY = os.getenv("MEM0_API_KEY")
MEM0_USER_ID = os.getenv("MEM0_USER_ID", "袋鼠")

if not MEM0_API_KEY:
    raise RuntimeError("Missing MEM0_API_KEY. Please set it in .env or environment variables.")

mem_client = MemoryClient(api_key=MEM0_API_KEY)

external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)

llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gpt-5-nano",
    openai_client=external_client,
)


def search_memories_for_user(query: str, user_id: str):
    return mem_client.search(
        query=query,
        filters={"user_id": user_id},
        top_k=3,
    )


@function_tool
async def search_user_memory(context: ToolContext[UserContext], query: str):
    """Use this tool to search user memories."""
    return search_memories_for_user(query=query, user_id=context.context.username)


@function_tool
async def save_user_memory(context: ToolContext[UserContext], query: str):
    """Use this tool to save user memories."""
    return mem_client.add(
        [{"role": "user", "content": query}],
        user_id=context.context.username,
    )


def dynamic_instructions_generator(
    context: RunContextWrapper[UserContext], agent: Agent[UserContext]
) -> str:
    response = search_memories_for_user(
        query="General Behavior",
        user_id=context.context.username,
    )
    print(response)
    return f"""你是一个个人助理，始终使用中文回答。
Use search_user_memory to find information and save_user_memory to remember information.
User Past Memories: {response}
"""


orchestrator_agent: Agent = Agent(
    name="DeepAgent",
    instructions=dynamic_instructions_generator,
    model=llm_model,
    tools=[save_user_memory, search_user_memory],
)


while True:
    input_text = input("\n [User:] ")
    if input_text.lower() in ["exit", "quit"]:
        break
    res = Runner.run_sync(
        orchestrator_agent,
        input_text,
        context=UserContext(username=MEM0_USER_ID),
    )
    print("\n [AGENT:]", res.final_output)
