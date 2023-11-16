from __future__ import annotations
from typing import TYPE_CHECKING
from grafanalib.core import GridPos

if TYPE_CHECKING:
    from grafanalib.core import Panel


class PanelArranger:
    def __init__(self):
        self.dashboard_space = []

    def find_available_space(self, desired_pos: GridPos) -> GridPos:
        if desired_pos.x + desired_pos.w > 24:
            raise ValueError("Panel width exceeds dashboard width")

        if len(self.dashboard_space) == 0:
            return GridPos(
                x=desired_pos.x, y=desired_pos.y, w=desired_pos.w, h=desired_pos.h
            )

        current_y = len(self.dashboard_space) - 1
        first_available_y = None

        while current_y >= 0:
            row = self.dashboard_space[current_y]
            row_is_available = all(
                not row[c] for c in range(desired_pos.x, desired_pos.x + desired_pos.w)
            )
            if row_is_available:
                first_available_y = current_y
            else:
                break
            current_y -= 1

        return GridPos(
            x=desired_pos.x, y=first_available_y, w=desired_pos.w, h=desired_pos.h
        )

    def arrange(self, panel: Panel) -> None:
        available_pos = self.find_available_space(panel.gridPos)
        panel.gridPos = available_pos
        self.occupy_space(panel.gridPos)

    def occupy_space(self, area: GridPos) -> None:
        # Allocate rows if needed
        while len(self.dashboard_space) <= area.y + area.h:
            self.dashboard_space.append([False for _ in range(24)])

        # Occupy space
        for y in range(area.y, area.y + area.h):
            for x in range(area.x, area.x + area.w):
                self.dashboard_space[y][x] = True
