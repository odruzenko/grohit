from cleo.application import Application as BaseApplication
from cleo.io.io import IO

from grohit.__version__ import __version__
from grohit.grohit import Grohit
from grohit.config.config import Settings


class Application(BaseApplication):
    def __init__(self):
        super().__init__("grohit", __version__)

        self._grohit: Grohit = None

    @property
    def grohit(self) -> Grohit:
        if self._grohit is not None:
            return self._grohit

        self._grohit = Grohit(Settings())
        return self._grohit

    def _run(self, io: IO) -> int:
        exit_code: int = super()._run(io)
        return exit_code
