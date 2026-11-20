import asyncio
import os

from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage

PROMPT = "Say hi"


async def main() -> None:
    # Agentic loop: streams messages as Claude works
    async for message in query(
        prompt=PROMPT,
        options=ClaudeAgentOptions(
            model=os.environ.get("MODEL", "qwen3.8:27b"),
            cwd=os.environ.get("CWD", "src/my_claude_agent"),
            system_prompt="You are a helpful assistant with Cloud SRE expertise. You can help with code review, debugging, and fixing issues in Compute program code.",
            max_turns=20,
            allowed_tools=["Read", "Glob"],  # Auto-approve these tools
            permission_mode="acceptEdits",  # Auto-approve file edits
            setting_sources=[],  # don't pull ~/.claude config in
            env={
                "ANTHROPIC_BASE_URL": os.environ.get(
                    "ANTHROPIC_BASE_URL", "http://localhost:11434"
                ),
                "ANTHROPIC_AUTH_TOKEN": os.environ.get("ANTHROPIC_AUTH_TOKEN", "ollama"),
                "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY", ""),
                "CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS": "1",
                "CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1",
            },
        ),
    ):
        # Print human-readable output
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)  # Claude's reasoning
                elif hasattr(block, "name"):
                    print(f"Tool: {block.name}")  # Tool being called
        elif isinstance(message, ResultMessage):
            print(f"Done: {message.subtype}")  # Final result


if __name__ == "__main__":
    asyncio.run(main())
