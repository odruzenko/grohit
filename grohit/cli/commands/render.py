import pathlib

from cleo.helpers import option
from rich.console import Console

from grohit.cli.commands.command import Command
from grohit.builder.dashboard import DashboardBuilder
from grohit.builder.utils import core_dashboard_to_json


class RenderCommand(Command):
    name = "render"
    description = "Renders Grafana dashboard by template"
    options = [
        option(
            long_name="template",
            short_name="t",
            description="Dashboard template",
            flag=False,
            multiple=True,
        ),
    ]

    def handle(self):
        template = self.option("template")
        if template is None:
            raise ValueError("template is required")

        tpl_file = str(pathlib.Path(template[0]).resolve())

        builder = DashboardBuilder()
        dashboard = builder.from_yaml(tpl_file)
        dashboard_json = core_dashboard_to_json(dashboard.build())

        console = Console()
        console.print(dashboard_json)
