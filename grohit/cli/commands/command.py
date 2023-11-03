from cleo.commands.command import Command as BaseCommand

from grohit.cli.app import Application
from grohit.grohit import Grohit


class Command(BaseCommand):
    @property
    def grohit(self) -> Grohit:
        return self.get_application().grohit

    def get_application(self) -> Application:
        application = self.application
        assert isinstance(application, Application)
        return application
