from __future__ import annotations
from typing import TYPE_CHECKING

import logging

from cleo.application import Application as BaseApplication
from cleo.events.console_events import COMMAND
from cleo.events.console_command_event import ConsoleCommandEvent
from cleo.events.event_dispatcher import EventDispatcher
from cleo.io.io import IO

from grohit.__version__ import __version__
from grohit.grohit import Grohit
from grohit.config.config import Settings

if TYPE_CHECKING:
    from cleo.events.event import Event


class Application(BaseApplication):
    def __init__(self):
        super().__init__("grohit", __version__)

        self._grohit: Grohit | None = None

        dispatcher = EventDispatcher()
        dispatcher.add_listener(COMMAND, self.register_command_loggers)
        self.set_event_dispatcher(dispatcher)

    @property
    def grohit(self) -> Grohit:
        if self._grohit is not None:
            return self._grohit

        self._grohit = Grohit(Settings())
        return self._grohit

    def register_command_loggers(
        self, event: Event, event_name: str, _: EventDispatcher
    ) -> None:
        assert isinstance(event, ConsoleCommandEvent)

        io = event.io

        level = logging.WARNING

        if io.is_debug():
            level = logging.DEBUG
        elif io.is_very_verbose() or io.is_verbose():
            level = logging.INFO

        logging.basicConfig(level=level)

    def _run(self, io: IO) -> int:
        logging.basicConfig(level=logging.INFO)
        exit_code = super()._run(io)
        return exit_code
