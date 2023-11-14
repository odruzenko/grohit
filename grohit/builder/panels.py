from __future__ import annotations
from typing import TYPE_CHECKING, List

from grafanalib.core import (
    RowPanel as CoreRowPanel,
)

from grohit.utils.loaders import load_class_by_name

if TYPE_CHECKING:
    from grafanalib.core import Panel as CorePanel


class Panel(object):
    def __init__(self, props: dict):
        self.props = props

    def build(self) -> List[CorePanel]:
        raise NotImplementedError("build() method not implemented")

    def _apply_config(self, panel: CorePanel):
        for k, v in self.props["config"].items():
            setattr(panel, k, v)


class RowPanel(Panel):
    def __init__(self, config: dict):
        super().__init__(config)

    def build(self) -> List[CoreRowPanel]:
        panel = CoreRowPanel(self.props["config"]["title"])
        self._apply_config(panel)
        return [panel]


class NativePanel(Panel):
    def __init__(self, config: dict):
        super().__init__(config)

    def build(self) -> List[CorePanel]:
        native_panel_type = self.props["native_panel_type"]
        native_panel_class = load_class_by_name(native_panel_type)
        panel = native_panel_class()
        self._apply_config(panel)
        return [panel]
