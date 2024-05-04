from fastapi import APIRouter
from starlette.requests import Request

from app.cqrs.room import CreateRoomCommand, GetRoomByQuery
from app.cqrs.user import CreateUserCommand

router_query = APIRouter(prefix="/api/queries", tags=["Queries"])


@router_query.get("/room")
async def get_room(request: Request, room_id: int):
    result = await request.app.state.mediator.send(
        GetRoomByQuery(id=room_id)
    )
    return result
