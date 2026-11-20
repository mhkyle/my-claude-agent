import asyncio

from dotenv import load_dotenv

from my_claude_agent.app import main

load_dotenv()

if __name__ == "__main__":
    asyncio.run(main())
