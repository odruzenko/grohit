from __future__ import annotations
from typing import TYPE_CHECKING
import json

from grohit.builder.dashboard import DashboardBuilder
from grohit.builder.utils import core_dashboard_to_json

if TYPE_CHECKING:
    from typing import Optional, Any
    from tests.types import FixtureDirGetter


def test_dashboard_config(fixture_dir: FixtureDirGetter) -> None:
    dashboard_yaml = str(fixture_dir("simple_dashboard") / "dashboard.yaml")

    builder = DashboardBuilder()
    dashboard = builder.from_yaml(dashboard_yaml)
    dashboard_json = core_dashboard_to_json(dashboard.build())
    dashboard_data = json.loads(dashboard_json)

    assert dashboard_data["title"] == "Simple Dashboard"
    assert dashboard_data["description"] == "This is a simple dashboard"
    assert dashboard_data["uid"] == "sdash"
    assert dashboard_data["id"] is None
    assert dashboard_data["timezone"] == "browser"
    assert not dashboard_data["editable"]
    assert dashboard_data["sharedCrosshair"]
    assert dashboard_data["tags"] == ["tag-1", "tag-2:simple2", "tag-3:simple3"]


def test_dashboard_config_overrides(fixture_dir: FixtureDirGetter) -> None:
    dashboard_yaml = str(fixture_dir("simple_dashboard") / "dashboard.yaml")

    config_overrides = {
        "title": "overridden title",
        "uid": "overridden",
        "id": 123,
    }

    builder = DashboardBuilder()
    dashboard = builder.from_yaml(dashboard_yaml, overrides=config_overrides)
    dashboard_json = core_dashboard_to_json(dashboard.build())
    dashboard_data = json.loads(dashboard_json)

    assert dashboard_data["title"] == "overridden title"
    assert dashboard_data["uid"] == "overridden"
    assert dashboard_data["id"] == 123


def test_dashboard_panels_build(fixture_dir: FixtureDirGetter) -> None:
    dashboard = build_test_dashboard(
        str(fixture_dir("native_panels") / "dashboard.yaml")
    )
    assert len(dashboard["panels"]) == 5
    assert dashboard["panels"][0]["type"] == "row"
    assert dashboard["panels"][0]["title"] == "Overview row"
    assert dashboard["panels"][1]["type"] == "stat"
    assert dashboard["panels"][1]["title"] == "Stat Panel 1"
    assert dashboard["panels"][1]["description"] == "This is a stat panel 1"


def build_test_dashboard(template_path: str, overrides: Optional[dict] = None) -> Any:
    builder = DashboardBuilder()
    dashboard = builder.from_yaml(template_path, overrides=overrides)
    dashboard_json = core_dashboard_to_json(dashboard.build())
    dashboard_data = json.loads(dashboard_json)
    return dashboard_data
