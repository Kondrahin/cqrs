from dataclasses import dataclass, field

from diator.events import DomainEvent, Event, EventHandler
from diator.requests import Request, RequestHandler
from diator.response import Response
from sqlalchemy.orm import Session
from app.orm.commands import engine as command_engine, Room
from app.orm.query import engine as query_engine, UserRoom


@dataclass(frozen=True, kw_only=True)
class CreateRoomCommand(Request):
    title: str = field()
    user_id: int = field()


@dataclass(frozen=True, kw_only=True)
class ReadRoomQueryResult(Response):
    id: int = field()
    title: str = field()
    user_id: int = field()
    first_name: str = field()
    last_name: str = field()


@dataclass(frozen=True, kw_only=True)
class GetRoomByQuery(Request):
    id: int = field()


@dataclass(frozen=True, kw_only=True)
class CreateRoomEvent(DomainEvent):
    title: str
    user_id: int


class CreateRoomCommandHandler(RequestHandler[CreateRoomCommand, None]):
    def __init__(self) -> None:
        self._events = []

    @property
    def events(self) -> list:
        return self._events

    async def handle(self, request: CreateRoomCommand) -> None:
        self._events.append(
            CreateRoomEvent(title=request.title, user_id=request.user_id)
        )


class GetRoomQueryHandler(RequestHandler[GetRoomByQuery, ReadRoomQueryResult]):
    def __init__(self) -> None:
        self._events: list[Event] = []

    async def handle(self, request: GetRoomByQuery) -> ReadRoomQueryResult:
        with Session(query_engine) as session:
            result = session.get(UserRoom, request.id)
        return ReadRoomQueryResult(
            id=result.id,
            title=result.title,
            user_id=result.user_id,
            first_name=result.first_name,
            last_name=result.last_name,
        )


class CreateRoomEventHandler(EventHandler[CreateRoomEvent]):
    async def handle(self, event: CreateRoomEvent) -> None:
        with Session(command_engine) as session:
            session.add(
                Room(
                    title=event.title,
                    user_id=event.user_id,
                )
            )
            session.commit()
        print("READY", event)
