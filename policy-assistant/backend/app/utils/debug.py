import json
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage,
    ToolMessage,
)


def print_messages(messages, title="Messages"):
    print("\n" + "=" * 60)
    print(f"🧠 {title}")
    print("=" * 60)

    for i, msg in enumerate(messages):
        role = type(msg).__name__

        print(f"\n--- Message {i+1} ({role}) ---")

        print("Content:")
        print(msg.content)

        if isinstance(msg, AIMessage):
            if msg.tool_calls:
                print("\n🔧 Tool Calls:")
                for tool_call in msg.tool_calls:
                    print(json.dumps(tool_call, indent=2))

        if isinstance(msg, ToolMessage):
            print("\n📦 Tool Output:")
            try:
                parsed = msg.content
                if isinstance(parsed, str):
                    parsed = json.loads(parsed)
                print(json.dumps(parsed[:2], indent=2))  # preview
            except Exception:
                print(msg.content)

    print("\n" + "=" * 60 + "\n")