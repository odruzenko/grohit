from __future__ import annotations
from typing import TYPE_CHECKING

import yaml
from dataclasses import dataclass

from pathlib import Path

if TYPE_CHECKING:
    from typing import Optional, Generator


class RegistryRecord:
    registry: Registry | None

    def __init__(self, registry: Registry | None = None):
        self.registry = registry


class Registry(RegistryRecord):
    id: str
    description: str
    _dashboard_folders: list[Folder]
    path: str | None = None
    _registries: list[Registry] | None = None

    def __init__(
        self,
        registry_id: str,
        description: str | None,
        dashboard_folders: list[Folder],
        registries: list[Registry] | None = None,
        registry: Registry | None = None,
        path: str | None = None,
    ):
        super().__init__(registry)
        self.id = registry_id
        self.description = description
        self._dashboard_folders = dashboard_folders
        self._registries = registries or []
        self.path = path

    @property
    def registries(self) -> Generator[Registry, None, None]:
        for registry in self._registries:
            yield registry
            for child_registry in registry.registries:
                yield child_registry

    @property
    def dashboard_folders(self) -> list[Folder]:
        return self._dashboard_folders

    @staticmethod
    def load(registry_path: str, parent_registry: Registry = None) -> Registry:
        path = str(Path(registry_path).resolve())

        with open(path) as f:
            registry_data = yaml.safe_load(f)

        registry = Registry(
            registry_id=registry_data["id"],
            description=registry_data.get("description", None),
            dashboard_folders=[],
            registry=parent_registry,
            path=path,
        )

        for child_registry_data in registry_data.get("registries", []):
            child_registry_path = child_registry_data["path"]
            child_registry_path = resolve_path(
                child_registry_path, str(Path(path).parent)
            )

            child_registry = Registry.load(child_registry_path, registry)
            registry._registries.append(child_registry)

        for folder_data in registry_data.get("dashboards", {}).get("folders", []):
            folder = Folder.load(folder_data, registry)
            registry.dashboard_folders.append(folder)

        return registry


@dataclass
class Folder(RegistryRecord):
    title: str
    uid: str
    dashboards: list[Dashboard]

    def __init__(
        self,
        title: str,
        uid: str,
        dashboards: list[Dashboard],
        registry: Registry | None = None,
    ):
        super().__init__(registry)
        self.title = title
        self.uid = uid
        self.dashboards = dashboards

    @staticmethod
    def load(folder_data: dict, registry: Registry) -> Folder:
        folder = Folder(
            registry=registry,
            title=folder_data["title"],
            uid=folder_data["uid"],
            dashboards=[],
        )
        for dashboard_data in folder_data.get("dashboards", []):
            dashboard = Dashboard.load(dashboard_data, registry, folder)
            folder.dashboards.append(dashboard)
        return folder


@dataclass
class Dashboard(RegistryRecord):
    uid: str
    title: str
    template_path: str
    folder: Folder

    def __init__(
        self,
        uid: str,
        title: str,
        template_path: str,
        folder: Folder,
        registry: Registry,
    ):
        super().__init__(registry)
        self.uid = uid
        self.title = title
        self.template_path = template_path
        self.folder = folder

    @property
    def path(self):
        return resolve_path(
            self.template_path, str(Path(self.folder.registry.path).parent)
        )

    @staticmethod
    def load(dashboard_data: dict, registry: Registry, folder: Folder) -> Dashboard:
        return Dashboard(
            registry=registry,
            title=dashboard_data["title"],
            uid=dashboard_data["uid"],
            template_path=dashboard_data["template"],
            folder=folder,
        )


class GrohitRegistry:
    def __init__(self):
        self._registries: list[Registry] = []

    def load_registry(self, registry_path: str):
        path = str(Path(registry_path).resolve())
        source_registry = Registry.load(path)
        self._registries.append(source_registry)

    @property
    def registries(self) -> Generator[Registry, None, None]:
        for registry in self._registries:
            yield registry
            for child_registry in registry.registries:
                yield child_registry

    @property
    def folders(self) -> Generator[Folder, None, None]:
        for registry in self.registries:
            for folder in registry.dashboard_folders:
                yield folder

    @property
    def dashboards(self) -> Generator[Dashboard, None, None]:
        for registry in self.registries:
            for folder in registry.dashboard_folders:
                for dashboard in folder.dashboards:
                    yield dashboard

    def get_dashboard(self, uid: str) -> Dashboard | None:
        for dashboard in self.dashboards:
            if dashboard.uid == uid:
                return dashboard
        return None


def resolve_path(path: str, relative_folder: Optional[str] = None):
    if path.startswith("/"):
        return path
    if relative_folder is None:
        return str(Path.resolve(path))

    return str(Path(relative_folder).resolve() / path)
