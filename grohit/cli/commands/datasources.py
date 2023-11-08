from rich.console import Console
from rich.table import Table

from grohit.cli.commands.command import Command


class ListDatasourcesCommand(Command):
    name = "list datasources"
    description = "List Grafana data sources"

    def handle(self):
        datasources = self.grohit.grafana_client.list_datasources()
        print(datasources)
        return

        table = Table(box=None)
        table.add_column("Title", style="cyan")
        table.add_column("UID")
        table.add_column("ID")

        for ds in datasources:
            table.add_row(ds["title"], ds["uid"], str(ds["id"]))

        console = Console()
        console.print(table)
