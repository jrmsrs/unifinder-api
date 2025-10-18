import asyncio
from fastapi import Request
from fastapi.responses import StreamingResponse
from typing import Dict, List

class SSEManager:
    def __init__(self):
        self.connections: Dict[str, List[asyncio.Queue]] = {}

    async def connect(self, user_id: str, request: Request) -> StreamingResponse:
        queue = asyncio.Queue()
        self.connections.setdefault(user_id, []).append(queue)

        async def event_generator():
            try:
                while True:
                    if await request.is_disconnected():
                        break
                    message = await queue.get()
                    yield f"data: {message}\n\n"
            finally:
                self.connections[user_id].remove(queue)
                if not self.connections[user_id]:
                    del self.connections[user_id]

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    async def send(self, user_id: str, message: str):
        if user_id not in self.connections:
            return
        for queue in self.connections[user_id]:
            await queue.put(message)

#instância global compartilhada
sse_manager = SSEManager()

def get_sse_manager() -> SSEManager:
    return sse_manager