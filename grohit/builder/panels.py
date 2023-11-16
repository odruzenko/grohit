from __future__ import annotations
from typing import TYPE_CHECKING, List

from grafanalib.core import (
    GridPos,
    RowPanel as CoreRowPanel,
)

from grohit.utils.loaders import load_class_by_name

if TYPE_CHECKING:
    from grafanalib.core import Panel as CorePanel


class Panel(object):
    def __init__(self, props: dict):
        self.props = props

    def build(self, position: GridPos) -> List[CorePanel]:
        raise NotImplementedError("build() method not implemented")

    def measure(self) -> GridPos:
        raise NotImplementedError("measure() method not implemented")

    def _apply_config(self, panel: CorePanel):
        for k, v in self.props["config"].items():
            setattr(panel, k, v)


class NativePanel(Panel):
    def __init__(self, props: dict):
        super().__init__(props)

    def build(self, position: GridPos) -> List[CorePanel]:
        native_panel_type = self.props["native_panel_type"]
        native_panel_class = load_class_by_name(native_panel_type)
        panel = native_panel_class()
        self._apply_config(panel)
        panel.gridPos = GridPos(
            x=position.x,
            y=position.y,
            w=self.props["grid_pos"]["w"],
            h=self.props["grid_pos"]["h"],
        )
        return [panel]

    def measure(self) -> GridPos:
        panel_x = self.props["grid_pos"]["x"]
        panel_w, panel_h = self.props["grid_pos"]["w"], self.props["grid_pos"]["h"]
        return GridPos(x=panel_x, y=0, w=panel_w, h=panel_h)


class RowPanel(Panel):
    def __init__(self, props: dict):
        super().__init__(props)

    def build(self, position: GridPos) -> List[CoreRowPanel]:
        panel = CoreRowPanel(self.props["config"]["title"])
        self._apply_config(panel)
        panel.gridPos = GridPos(
            x=0,
            y=position.y,
            w=24,
            h=1,
        )
        return [panel]

    def measure(self) -> GridPos:
        return GridPos(x=0, y=0, w=24, h=1)
