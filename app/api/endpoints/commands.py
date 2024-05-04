from fastapi import APIRouter
from starlette.requests import Request

from app.cqrs.room import CreateRoomCommand
from app.cqrs.user import CreateUserCommand

router_commands = APIRouter(prefix="/api/commands", tags=["Commands"])


@router_commands.post("/user")
async def create_user(request: Request, first_name: str, last_name: str):
    await request.app.state.mediator.send(
        CreateUserCommand(first_name=first_name, last_name=last_name)
    )


@router_commands.post("/room")
async def create_room(
    request: Request,
    title: str,
    user_id: int,
):
    result = await request.app.state.mediator.send(
        CreateRoomCommand(title=title, user_id=user_id)
    )
    print(result)
