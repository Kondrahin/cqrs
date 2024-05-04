from di import Container, bind_by_type
from di.dependent import Dependent
from diator.container.di import DIContainer

from app.cqrs.room import CreateRoomCommandHandler, CreateRoomEventHandler


def configure_di() -> DIContainer:
    container = Container()

    container.bind(
        bind_by_type(
            Dependent(CreateRoomEventHandler, scope="request"), CreateRoomEventHandler
        )
    )
    container.bind(
        bind_by_type(
            Dependent(CreateRoomCommandHandler, scope="request"),
            CreateRoomCommandHandler,
        )
    )

    di_container = DIContainer()
    di_container.attach_external_container(container)

    return di_container
