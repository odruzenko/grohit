from grohit.cli.app import Application
from grohit.cli.commands.folders import ListFoldersCommand
from grohit.cli.commands.dashboards import (
    GetDashboardCommand,
    ListDashboardsCommand,
    UploadDashboardCommand,
)
from grohit.cli.commands.datasources import ListDatasourcesCommand


def run() -> int:
    app = Application()
    app.add(ListFoldersCommand())
    app.add(ListDatasourcesCommand())
    app.add(ListDashboardsCommand())
    app.add(GetDashboardCommand())
    app.add(UploadDashboardCommand())
    return app.run()


if __name__ == "__main__":
    run()
