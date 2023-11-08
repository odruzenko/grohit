from rich.console import Console
from rich.table import Table

from grohit.cli.commands.command import Command


class ListFoldersCommand(Command):
    name = "list folders"
    description = "List Grafana folders"

    def handle(self):
        folders = self.grohit.grafana_client.list_folders()

        table = Table(box=None)
        table.add_column("Title", style="cyan")
        table.add_column("UID")
        table.add_column("ID")

        for folder in folders:
            table.add_row(folder["title"], folder["uid"], str(folder["id"]))

        console = Console()
        console.print(table)
