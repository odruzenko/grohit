from __future__ import annotations
from typing import TYPE_CHECKING
from abc import abstractmethod
from importlib import metadata

if TYPE_CHECKING:
    from grohit.registry.registry import GrohitRegistry


class RegistryPlugin:
    group = "grohit.registry_plugin"

    @abstractmethod
    def activate(self, registry: GrohitRegistry) -> None:
        raise NotImplementedError


class RegistryPluginManager:
    def __init__(self, registry: GrohitRegistry):
        self.registry = registry

    def load_plugins(self) -> None:
        plugin_entry_points = RegistryPluginManager.get_plugin_entry_points()
        for ep in plugin_entry_points:
            plugin_class = ep.load()
            plugin = plugin_class()
            plugin.activate(self.registry)

    @staticmethod
    def get_plugin_entry_points() -> list[metadata.EntryPoint]:
        return metadata.entry_points(group=RegistryPlugin.group)
