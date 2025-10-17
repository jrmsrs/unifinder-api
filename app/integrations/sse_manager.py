import asyncio
from fastapi import Request
from fastapi.responses import StreamingResponse
from typing import Dict, List


class SSEManager:
    def __init__(self):
        self.connections: Dict[str, List[asyncio.Queue]] = {}

    async def connect(self, user_id: str, request: Request):
        queue = asyncio.Queue()
        if user_id not in self.connections:
            self.connections[user_id] = []
        self.connections[user_id].append(queue)

        async def event_generator():
            while True:
                if await request.is_disconnected():
                    self.connections[user_id].remove(queue)
                    break
                message = await queue.get()
                yield f"data: {message}\n\n"

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    async def send(self, user_id: str, message: str):
        if user_id in self.connections:
            for queue in self.connections[user_id]:
                await queue.put(message)
