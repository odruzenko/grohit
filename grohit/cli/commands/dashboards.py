import os.path
import json
from cleo.helpers import option
from rich.console import Console
from rich.table import Table

from grohit.cli.commands.command import Command


class ListDashboardsCommand(Command):
    name = "list dashboards"
    description = "List Grafana dashboards"
    options = [
        option(
            long_name="folder",
            short_name="f",
            description="The folder id (int) to list dashboards from",
            flag=False,
            value_required=True,
        ),
        option(
            long_name="tag",
            short_name="t",
            description="Filter by tag",
            flag=False,
            multiple=True,
        ),
    ]

    def handle(self):
        folder_id = self.option("folder")
        tags = self.option("tag")

        if folder_id is None and not tags:
            raise ValueError("folder id or tag is required")

        dashboards = self.grohit.grafana_client.list_dashboards(
            folder_id=folder_id, tags=tags
        )

        table = Table(box=None)
        table.add_column("Title", style="cyan")
        table.add_column("UID")
        table.add_column("ID")
        table.add_column("Tags")
        table.add_column("URL")
        table.add_column("Folder")

        for dashboard in dashboards:
            table.add_row(
                dashboard["title"],
                dashboard["uid"],
                str(dashboard["id"]),
                ", ".join(dashboard["tags"]),
                self.grohit.grafana_url + dashboard["url"],
                dashboard["folderTitle"] if "folderTitle" in dashboard else "",
            )

        console = Console()
        console.print(table)


class GetDashboardCommand(Command):
    name = "get dashboard"
    description = "Get Grafana dashboard"
    options = [
        option(
            long_name="uid",
            short_name="u",
            description="The dashboard uid (str) to get",
            flag=False,
            value_required=True,
        )
    ]

    def handle(self):
        uid = self.option("uid")
        if uid is None:
            raise ValueError("dashboard uid is required")

        dashboard = self.grohit.grafana_client.get_dashboard(uid=uid)

        console = Console()
        console.print(json.dumps(dashboard, indent=2))


class UploadDashboardCommand(Command):
    name = "upload dashboard"
    description = "Upload Grafana dashboard"
    options = [
        option(
            long_name="file",
            short_name="i",
            description="The dashboard file (str) to upload",
            flag=False,
            value_required=True,
        ),
        option(
            long_name="response",
            short_name="r",
            description="Input file is a Grafana API dashboard response",
            flag=True,
        ),
        option(
            long_name="folder-uid",
            description="The folder uid (str) to upload the dashboard to",
            flag=False,
        ),
        option(
            long_name="folder-id",
            description="The folder id (int) to upload the dashboard to",
            flag=False,
        ),
        option(
            long_name="auto-version",
            description="Automatically update the dashboard version if it already exists",
            flag=True,
        ),
        option(
            long_name="overwrite", description="Overwrite existing dashboard", flag=True
        ),
    ]

    def handle(self):
        file = self.option("file")
        if file is None:
            raise ValueError("dashboard file is required")

        # Get file path taking into account relative paths
        file = self.get_file_path(file)
        with open(file, "r") as f:
            content = f.read()
        file_data = json.loads(content)

        is_response_format = self.option("response")
        if is_response_format:
            print("Upload response data")
            upload_response = self.grohit.grafana_uploader.upload_from_response_data(
                file_data,
                auto_version=self.option("auto-version"),
                overwrite=self.option("overwrite"),
                folder_uid=self.option("folder-uid"),
                folder_id=self.option("folder-id"),
            )
        else:
            upload_response = self.grohit.grafana_uploader.upload(
                file_data,
                auto_version=self.option("auto-version"),
                overwrite=self.option("overwrite"),
                folder_uid=self.option("folder-uid"),
                folder_id=self.option("folder-id"),
            )

        console = Console()
        console.print(upload_response)

    def get_file_path(self, file: str):
        if file.startswith("/"):
            return file
        else:
            return os.path.join(os.getcwd(), file)
