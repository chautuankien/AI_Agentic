from langgraph.graph.state import CompiledStateGraph
from langchain_core.messages import BaseMessage
from typing import Optional

async def print_stream(app: CompiledStateGraph, input: str) -> Optional[BaseMessage]:
    print("## New research running")
    print(f"### Input:\n\n{input}\n\n")
    print("### Stream:\n\n")

    # Stream the results
    all_messages: list = []
    async for chunk in app.astream({"messages": [input]}, stream_mode="updates"):
        print(chunk)
        for updates in chunk.values():
            if messages:= updates.get("messages"):
                all_messages.extend(messages)
                for message in messages:
                    message.pretty_print()
                    print("\n\n")
    # Return the last message if any
    if not all_messages:
        return None
    return all_messages[-1]