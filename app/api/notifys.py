from fastapi import APIRouter, Depends, Request
from app.integrations.sse_manager import SSEManager, get_sse_manager

router = APIRouter()


@router.get("/sse/{user_id}")
async def sse_endpoint(
    user_id: str,
    request: Request,
    sse_manager: SSEManager = Depends(get_sse_manager)
):
    return await sse_manager.connect(user_id, request)
