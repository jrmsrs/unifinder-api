import asyncio
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

router = APIRouter()
connections = {}

@router.get("/sse/{user_id}")
async def sse(user_id: str, request: Request):
    queue = asyncio.Queue()
    
    connections[user_id] = queue

    async def event_generator():
        while True:
            if await request.is_disconnected():
                break
            message = await queue.get()
            yield f"data: {message}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.post("/{user_id}")
async def notify(user_id: str, message: str):
    if user_id in connections:
        await connections[user_id].put(message)
        return {"status": "notificado"}
    return {"error": "usuário não conectado"}