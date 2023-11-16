from __future__ import annotations
from typing import TYPE_CHECKING
from cleo.commands.command import Command as BaseCommand
from grohit.cli.app import Application

if TYPE_CHECKING:
    from grohit.grohit import Grohit


class Command(BaseCommand):
    @property
    def grohit(self) -> Grohit:
        return self.get_application().grohit

    def get_application(self) -> Application:
        application = self.application
        assert isinstance(application, Application)
        return application
