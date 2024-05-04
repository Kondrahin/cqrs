from diator.requests import Request
from sqlalchemy.orm import Session

from app.cqrs.room import CreateRoomCommand
from app.orm.query import engine as query_engine, UserRoom
from app.orm.commands import engine as command_engine, User


class Synchronizer:
    async def __call__(self, request: Request, handle):
        response = await handle(request)
        if isinstance(request, CreateRoomCommand):
            request: CreateRoomCommand
            with Session(command_engine) as session:
                user = session.get(User, request.user_id)
            with Session(query_engine) as session:
                session.add(
                    UserRoom(
                        title=request.title,
                        user_id=request.user_id,
                        first_name=user.first_name,
                        last_name=user.last_name,
                    )
                )
                session.commit()
        return response
