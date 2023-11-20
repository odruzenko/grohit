from __future__ import annotations
from typing import TYPE_CHECKING

from grohit.registry.registry import GrohitRegistry

if TYPE_CHECKING:
    from tests.types import FixtureDirGetter


def test_registry_load(fixture_dir: FixtureDirGetter) -> None:
    registry_yaml = str(fixture_dir("registry") / "registry1.yaml")

    registry = GrohitRegistry()
    registry.load_registry(registry_yaml)

    assert len(list(registry.folders)) == 2


def test_meta_registry(fixture_dir: FixtureDirGetter) -> None:
    registry_yaml = str(fixture_dir("registry") / "meta_registry.yaml")

    registry = GrohitRegistry()
    registry.load_registry(registry_yaml)

    assert len(list(registry.registries)) == 3
    assert len(list(registry.folders)) == 3
    assert len(list(registry.dashboards)) == 5
