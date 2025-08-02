# tool_manager.py
import os
import importlib.util
import inspect
import redis
from agno.agent import Agent

# Connect to Redis using environment variables
redis_client = redis.Redis(
    host=os.getenv("REDISHOST", "localhost"),
    port=os.getenv("REDISPORT", 6379),
    password=os.getenv("REDISPASSWORD"),
    decode_responses=True
)

def save_tool_to_redis(agent: Agent, tool_name: str, tool_code: str) -> str:
    """Saves the Python code for a new, validated tool to Redis."""
    try:
        redis_client.hset("dynamic_tools", tool_name, tool_code)
        # Immediately load the new tool into the currently running agent
        load_single_tool(agent, tool_name, tool_code)
        return f"Tool '{tool_name}' has been successfully created, tested, and loaded for immediate use."
    except Exception as e:
        return f"Error saving tool to Redis: {e}"

def load_single_tool(agent: Agent, tool_name: str, tool_code: str):
    """Dynamically creates a Python module from code and adds the tool function to the agent."""
    try:
        # Create a module specification and module from the tool code
        spec = importlib.util.spec_from_loader(tool_name, loader=None)
        if spec is None:
            raise ImportError(f"Could not create spec for module {tool_name}")
        
        module = importlib.util.module_from_spec(spec)
        exec(tool_code, module.__dict__)

        # Find the function within the newly created module
        tool_func = next((obj for name, obj in inspect.getmembers(module) if inspect.isfunction(obj) and name == tool_name), None)
        
        if tool_func:
            agent.add_tool(tool_func)
            print(f"✅ Dynamically loaded tool: {tool_name}")
        else:
            print(f"❌ Could not find function '{tool_name}' in the provided code.")
            
    except Exception as e:
        print(f"Error loading tool '{tool_name}': {e}")

def load_all_tools_from_redis(agent: Agent):
    """Loads all saved tools from Redis into the agent instance at startup."""
    print("Loading dynamic tools from Redis...")
    try:
        tools = redis_client.hgetall("dynamic_tools")
        if not tools:
            print("No dynamic tools found in Redis.")
            return
        for tool_name, tool_code in tools.items():
            load_single_tool(agent, tool_name, tool_code)
        print(f"Loaded {len(tools)} dynamic tools.")
    except redis.exceptions.ConnectionError as e:
        print(f"❌ Could not connect to Redis: {e}")
        print("Skipping dynamic tool loading. Please check your Redis connection variables.")
    except Exception as e:
        print(f"An unexpected error occurred while loading tools from Redis: {e}")
