from rich.console import Console
from rich.table import Table

from grohit.cli.commands.command import Command


class RenderCommand(Command):
    """
    Render a template
    render
        {template : The template file}
        {--o|output= : The output file}
        {--d|data= : The data file}
    """

    name = "render"
    description = "Renders Grafana dashboard by template"

    def handle(self):
        print("test")
        folders = self.grohit.grafana_client.list_folders()

        table = Table(box=None)
        table.add_column("Title", style="cyan")
        table.add_column("UID")
        table.add_column("ID")
        for folder in folders:
            table.add_row(folder["title"], folder["uid"], str(folder["id"]))

        console = Console()
        console.print(table)
