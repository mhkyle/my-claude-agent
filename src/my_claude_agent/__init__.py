import asyncio
import sys

from dotenv import load_dotenv


def main(prompt: str | None = None) -> None:
    """Console-script entry point: runs the agent for one request."""
    load_dotenv()
    from .agent import main as agent_main

    if prompt is None:
        if len(sys.argv) < 2:
            sys.exit('usage: my-claude-agent "your request"')
        prompt = " ".join(sys.argv[1:])
    asyncio.run(agent_main(prompt))
