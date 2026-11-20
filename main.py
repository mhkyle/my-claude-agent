import asyncio
import sys

from dotenv import load_dotenv

from my_claude_agent.agent import main

load_dotenv()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('usage: uv run main.py "your request"')
    asyncio.run(main(" ".join(sys.argv[1:])))
