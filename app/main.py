from diator.events import EventMap, EventEmitter
from diator.mediator import Mediator
from diator.middlewares import MiddlewareChain
from diator.requests import RequestMap
from fastapi import FastAPI

from app.api.routers import router
from app.cqrs.base import configure_di
from app.cqrs.middleware import Synchronizer
from app.cqrs.user import (
    CreateUserCommandHandler,
    CreateUserCommand,
    CreateUserEvent,
    CreateUserEventHandler,
)
from app.cqrs.room import (
    CreateRoomCommandHandler,
    CreateRoomEventHandler,
    CreateRoomEvent,
    CreateRoomCommand, GetRoomByQuery, GetRoomQueryHandler,
)

app = FastAPI()
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    middleware_chain = MiddlewareChain()
    middleware_chain.add(Synchronizer())

    event_map = EventMap()
    event_map.bind(CreateUserEvent, CreateUserEventHandler)
    event_map.bind(CreateRoomEvent, CreateRoomEventHandler)
    request_map = RequestMap()
    request_map.bind(CreateUserCommand, CreateUserCommandHandler)
    request_map.bind(CreateRoomCommand, CreateRoomCommandHandler)
    request_map.bind(GetRoomByQuery, GetRoomQueryHandler)
    container = configure_di()

    event_emitter = EventEmitter(
        event_map=event_map,
        container=container,
    )

    app.state.mediator = Mediator(
        request_map=request_map,
        event_emitter=event_emitter,
        container=container,
        middleware_chain=middleware_chain,
    )
