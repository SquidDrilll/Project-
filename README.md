# README.md
# Dynamic Discord Agent with Agno

This project is a Discord self-bot powered by the Agno framework. It can dynamically create, test, and store new tools on the fly using natural language commands.

**Disclaimer:** Using a self-bot is a violation of Discord's Terms of Service and can result in account termination. This project is for educational purposes only.

## Features

-   **Dynamic Tool Creation**: Tell the bot to create a new tool by describing what it should do.
-   **AI-Powered Code Generation**: Uses Groq's LLaMA 3.1 70B model to write Python code for new tools.
-   **Sandboxed Testing**: Securely tests all new code in a Daytona sandbox before saving.
-   **Persistent Tool Storage**: Stores validated tools in a Redis database for future use.
-   **On-Demand Execution**: Call any dynamically created tool from Discord.

## Setup & Deployment on Railway

1.  **Fork this Repository**: Create your own copy of this repository on GitHub.
2.  **Create a Railway Project**:
    -   Go to [railway.app](https://railway.app) and create a new project.
    -   Deploy from your GitHub repo. Railway will automatically detect the `Procfile`.
3.  **Add a Redis Service**:
    -   In your Railway project, click "+ New" and select "Database" -> "Redis".
    -   Railway will automatically link this database to your `worker` service and provide the necessary environment variables (`REDISHOST`, `REDISPORT`, `REDISPASSWORD`).
4.  **Configure Environment Variables**:
    -   In your Railway project's "Variables" tab, add the following secrets:
        -   `DISCORD_TOKEN`: Your Discord user token.
        -   `GROQ_API_KEY`: Your Groq API key.
        -   `DAYTONA_API_KEY`: Your Daytona API key.
        -   `FIREcrawl_API_KEY`: Your Firecrawl API key.

## Usage

Once deployed and running, you can interact with the bot in any Discord channel.

-   **Create a new tool**:
    `!do create tool to get the current price of a cryptocurrency using the CoinGecko API`

-   **Execute a tool**:
    `!do get_crypto_price coin=bitcoin`
