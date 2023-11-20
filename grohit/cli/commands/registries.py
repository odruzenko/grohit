import logging
from rich.console import Console
from rich.table import Table

from grohit.cli.commands.command import Command


logger = logging.getLogger(__name__)


class ListRegistriesCommand(Command):
    name = "registry list registries"
    description = "List registered Grohit registries"

    def handle(self):
        table = Table(box=None)
        table.add_column("ID", style="cyan")
        table.add_column("Description")
        table.add_column("Path")

        for registry in self.grohit.registry.registries:
            table.add_row(registry.id, registry.description, registry.path)

        console = Console()
        console.print(table)


class ListRegistryFoldersCommand(Command):
    name = "registry list folders"
    description = "List registered folders"

    def handle(self):
        table = Table(box=None)
        table.add_column("UID", style="cyan")
        table.add_column("Title")
        table.add_column("Registry ID")

        for folder in self.grohit.registry.folders:
            table.add_row(folder.uid, folder.title, folder.registry.id)

        console = Console()
        console.print(table)


class ListRegistryDashboardsCommand(Command):
    name = "registry list dashboards"

    description = "List registered dashboards"

    def handle(self):
        table = Table(box=None)
        table.add_column("UID", style="cyan")
        table.add_column("Title")
        table.add_column("Path")
        table.add_column("Folder UID")
        table.add_column("Folder Title")
        table.add_column("Registry ID")

        for dashboard in self.grohit.registry.dashboards:
            table.add_row(
                dashboard.uid,
                dashboard.title,
                dashboard.path,
                dashboard.folder.uid,
                dashboard.folder.title,
                dashboard.registry.id,
            )

        console = Console()
        console.print(table)
