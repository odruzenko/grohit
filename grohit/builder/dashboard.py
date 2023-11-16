from __future__ import annotations
from typing import TYPE_CHECKING, List

import yaml

from grafanalib.core import Dashboard as CoreDashboard
from grohit.utils.loaders import load_class_by_name
from grohit.builder.arrangment import PanelArranger

if TYPE_CHECKING:
    from grohit.builder.panels import Panel
    from grohit.builder.registry import TemplateRegistry


class Dashboard:
    def __init__(self, config: dict, panels: List[Panel] = None):
        self.config = config
        self.panels = panels

    def build(self) -> CoreDashboard:
        board = CoreDashboard(self.config["title"])
        self._apply_config(board)
        self._apply_panels(board)
        board = board.auto_panel_ids()
        return board

    def _apply_config(self, board: CoreDashboard):
        for k, v in self.config.items():
            if k == "title":
                continue
            setattr(board, k, v)

    def _apply_panels(self, board: CoreDashboard):
        if not self.panels:
            return

        arranger = PanelArranger()
        for panel in self.panels:
            desired_pos = panel.measure()
            available_pos = arranger.find_available_space(desired_pos)

            panels = panel.build(position=available_pos)
            for p in panels:
                arranger.arrange(p)
                board.panels.append(p)


class DashboardBuilder:
    def __init__(self, template_registry: TemplateRegistry = None):
        self.template_registry = template_registry

    def from_template(self, template, overrides: dict = None) -> Dashboard:
        config = template["config"]
        if overrides:
            config = {**config, **overrides}

        panels = []
        if "panels" in template and template["panels"]:
            for panel_config in template["panels"]:
                panel_type = panel_config["type"]
                panel_class = load_class_by_name(panel_type)
                panel = panel_class(panel_config)
                panels.append(panel)

        return Dashboard(config, panels)

    def from_yaml(self, yaml_file: str, overrides: dict = None) -> Dashboard:
        with open(yaml_file, "r") as f:
            yaml_data = yaml.safe_load(f)
        return self.from_template(yaml_data, overrides)
