import json
from typing import AsyncGenerator
from langchain_core.messages import HumanMessage
from app.graphs.workflow import build_graph
from app.core.app_logging import get_logger
import asyncio

logger = get_logger(__name__)


class ChatService:
    def __init__(self):
        self.graph = build_graph()

    async def stream_chat(self, message: str):
        try:
            state = {
                "user_question": message,
                "messages": [HumanMessage(content=message)],
            }

            final_state = None

            async for event in self.graph.astream_events(state, version="v1"):
                event_type = event["event"]

                if event_type == "on_chat_model_stream":
                    chunk = event["data"]["chunk"]

                    if chunk.content:
                        yield json.dumps({
                            "type": "token",
                            "content": chunk.content,
                        }) + "\n"

                        await asyncio.sleep(0)

                elif event_type == "on_chain_end":
                    final_state = event["data"]["output"]

            if final_state:
                guardrail_output = final_state["guardrail"]

                yield json.dumps({
                    "type": "final",
                    "answer": guardrail_output.get("final_answer", ""),
                    "sources": guardrail_output.get("citations", []),
                }) + "\n"

            yield json.dumps({
                "type": "done"
            }) + "\n"

        except Exception as e:
            print("STREAM ERROR:", e)

            yield json.dumps({
                "type": "error",
                "message": str(e),
            }) + "\n"

