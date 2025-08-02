# main.py
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from master_agent import master_agent
from tool_manager import load_all_tools_from_redis

# IMPORTANT: Using a self-bot is against Discord's Terms of Service
# and can result in your account being terminated. This is for educational purposes only.

# Load environment variables from a .env file for local development
load_dotenv()

# At startup, load all previously created tools from Redis into the agent's memory
load_all_tools_from_redis(master_agent)

# Discord Bot Setup
bot = commands.Bot(command_prefix="!", self_bot=True)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print('------')

@bot.command(name='do')
async def execute_command(ctx, *, prompt: str):
    """Main command to interact with the Master Agent."""
    
    # Indicate that the bot is processing the request
    async with ctx.typing():
        print(f"Received command from Discord: {prompt}")
        
        # Run the agent asynchronously to avoid blocking the bot
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, master_agent.run, prompt)
        
        # Send the final response back to the Discord channel
        if response and response.content:
            content = str(response.content)
            # Discord has a 2000 character limit per message
            for chunk in [content[i:i+1950] for i in range(0, len(content), 1950)]:
                await ctx.send(f"```\n{chunk}\n```")
        else:
            await ctx.send("The agent did not produce a response.")

# Run the bot using the token from your environment variables
bot.run(os.getenv("DISCORD_TOKEN"))
