import asyncio

from dotenv import load_dotenv


def main() -> None:
    """Console-script entry point: runs the agent loop."""
    load_dotenv()
    from .app import main as agent_main

    asyncio.run(agent_main())
