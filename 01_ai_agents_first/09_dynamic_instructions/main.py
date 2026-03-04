# 🎭 Dynamic Instructions: Make Your Agent Adapt
# Simple examples to learn dynamic instructions

import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, RunContextWrapper

# 🌿 Load environment variables
load_dotenv()
set_tracing_disabled(disabled=True)

# 🔐 Setup Gemini client
API_KEY = os.getenv("AIHUBMIX_API_KEY")
BASE_URL = os.getenv("AIHUBMIX_BASE_URL")

external_client = AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL)
model = OpenAIChatCompletionsModel(model="gpt-4o", openai_client=external_client)

def main():
    """Learn Dynamic Instructions with simple examples."""
    print("🎭 Dynamic Instructions: Make Your Agent Adapt")
    print("=" * 50)
    
    # 🎯 Example 1: Basic Dynamic Instructions
    print("\n🎭 Example 1: Basic Dynamic Instructions")
    print("-" * 40)
    
    def basic_dynamic(context: RunContextWrapper, agent: Agent) -> str:
        """Basic dynamic instructions function."""
        return f"You are {agent.name}. Be helpful and friendly. 必须说中文。"
    
    agent_basic = Agent(
        name="Dynamic Agent",
        instructions=basic_dynamic,
        model=model
    )
    
    result = Runner.run_sync(agent_basic, "Hello!")
    print("Basic Dynamic Agent:")
    print(result.final_output)
    
    # 🎯 Example 2: Context-Aware Instructions
    print("\n🎭 Example 2: Context-Aware Instructions")
    print("-" * 40)
    
    def context_aware(context: RunContextWrapper, agent: Agent) -> str:
        """Context-aware instructions based on message count."""
        message_count = len(getattr(context, 'messages', []))
        
        if message_count == 0:
            return "You are a welcoming assistant. Introduce yourself! 必须说中文。"
        elif message_count < 3:
            return "You are a helpful assistant. Be encouraging and detailed. 必须说中文。"
        else:
            return "You are an experienced assistant. Be concise but thorough. 必须说中文。"
    
    agent_context = Agent(
        name="Context Aware Agent",
        instructions=context_aware,
        model=model
    )
    
    # Test with multiple messages
    result1 = Runner.run_sync(agent_context, "Hello!")
    print("First message:")
    print(result1.final_output)
    
    result2 = Runner.run_sync(agent_context, "Tell me about Python")
    print("\nSecond message:")
    print(result2.final_output)
    
    # 🎯 Example 3: Time-Based Instructions
    print("\n🎭 Example 3: Time-Based Instructions")
    print("-" * 40)
    
    import datetime
    
    def time_based(context: RunContextWrapper, agent: Agent) -> str:
        """Time-based instructions based on current hour."""
        current_hour = datetime.datetime.now().hour
        
        if 6 <= current_hour < 12:
            return f"You are {agent.name}. Good morning! Be energetic and positive. 必须说中文。"
        elif 12 <= current_hour < 17:
            return f"You are {agent.name}. Good afternoon! Be focused and productive. "
        else:
            return f"You are {agent.name}. Good evening! Be calm and helpful. 必须说中文。"
    
    agent_time = Agent(
        name="Time Aware Agent",
        instructions=time_based,
        model=model
    )
    
    result = Runner.run_sync(agent_time, "How are you today?")
    print("Time-Based Agent:")
    print(result.final_output)
    
    # 🎯 Example 4: Stateful Instructions (Remembers)
    print("\n🎭 Example 4: Stateful Instructions")
    print("-" * 40)
    
    class StatefulInstructions:
        """Stateful instructions that remember interaction count."""
        def __init__(self):
            self.interaction_count = 0
        
        def __call__(self, context: RunContextWrapper, agent: Agent) -> str:
            self.interaction_count += 1
            
            if self.interaction_count == 1:
                return "You are a learning assistant. This is our first interaction - be welcoming! 必须说中文。"
            elif self.interaction_count <= 3:
                return f"You are a learning assistant. This is interaction #{self.interaction_count} - build on our conversation. 必须说中文。"
            else:
                return f"You are an experienced assistant. We've had {self.interaction_count} interactions - be efficient. 必须说中文。"
    
    instruction_gen = StatefulInstructions()
    
    agent_stateful = Agent(
        name="Stateful Agent",
        instructions=instruction_gen,
        model=model
    )
    
    # Test multiple interactions
    for i in range(3):
        result = Runner.run_sync(agent_stateful, f"Question {i+1}: Tell me about AI")
        print(f"Interaction {i+1}:")
        print(result.final_output[:100] + "...")
        print()
    
    # 🎯 Example 5: Exploring Context and Agent
    print("\n🎭 Example 5: Exploring Context and Agent")
    print("-" * 40)
    
    def explore_context_and_agent(context: RunContextWrapper, agent: Agent) -> str:
        """Explore what's available in context and agent."""
        # Access conversation messages
        messages = getattr(context, 'messages', [])
        message_count = len(messages)
        
        # Access agent properties
        agent_name = agent.name
        tool_count = len(agent.tools)
        
        return f"""You are {agent_name} with {tool_count} tools. 
        This is message #{message_count} in our conversation.
        Be helpful and informative! 必须说中文。"""
    
    agent_explorer = Agent(
        name="Context Explorer",
        instructions=explore_context_and_agent,
        model=model
    )
    
    result = Runner.run_sync(agent_explorer, "What can you tell me about yourself?")
    print("Context Explorer Agent:")
    print(result.final_output)
    
    print("\n🎉 You've learned Dynamic Instructions!")
    print("💡 Try changing the functions and see what happens!")

if __name__ == "__main__":
    main()