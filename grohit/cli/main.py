from grohit.cli.app import Application
from grohit.cli.commands.folders import ListFoldersCommand
from grohit.cli.commands.dashboards import (
    GetDashboardCommand,
    ListDashboardsCommand,
    UploadDashboardCommand,
)
from grohit.cli.commands.render import RenderCommand
from grohit.cli.commands.datasources import ListDatasourcesCommand
from grohit.cli.commands.registries import (
    ListRegistriesCommand,
    ListRegistryFoldersCommand,
    ListRegistryDashboardsCommand,
)


def run() -> int:
    app = Application()
    app.add(ListFoldersCommand())
    app.add(ListDatasourcesCommand())
    app.add(ListDashboardsCommand())
    app.add(GetDashboardCommand())
    app.add(UploadDashboardCommand())
    app.add(RenderCommand())
    app.add(ListRegistriesCommand())
    app.add(ListRegistryFoldersCommand())
    app.add(ListRegistryDashboardsCommand())
    return app.run()


if __name__ == "__main__":
    run()
