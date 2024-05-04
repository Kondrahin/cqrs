from dataclasses import dataclass, field
from diator.events import (
    DomainEvent,
    EventHandler,
)
from diator.requests import Request, RequestHandler
from diator.response import Response

from sqlalchemy.orm import Session
from app.orm.commands import engine as command_engine, User


@dataclass(frozen=True, kw_only=True)
class CreateUserCommand(Request):
    first_name: str = field()
    last_name: str = field()


@dataclass(frozen=True, kw_only=True)
class CreateUserQueryResult(Response):
    room_id: int = field()
    user_id: int = field()


@dataclass(frozen=True, kw_only=True)
class CreateUserEvent(DomainEvent):
    first_name: str = field()
    last_name: str = field()


class CreateUserCommandHandler(RequestHandler[CreateUserCommand, None]):
    def __init__(self) -> None:
        self._events = []

    @property
    def events(self) -> list:
        return self._events

    async def handle(self, request: CreateUserCommand) -> None:
        self._events.append(
            CreateUserEvent(first_name=request.first_name, last_name=request.last_name)
        )


class CreateUserEventHandler(EventHandler[CreateUserEvent]):
    async def handle(self, event: CreateUserEvent) -> None:
        with Session(command_engine) as session:
            session.add(
                User(
                    first_name=event.first_name,
                    last_name=event.last_name,
                )
            )
            session.commit()

        print("READY", event)
