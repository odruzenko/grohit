from grohit.cli.app import Application
from grohit.cli.commands.render import RenderCommand


def run() -> int:
    app = Application()
    app.add(RenderCommand())
    return app.run()


if __name__ == "__main__":
    run()
