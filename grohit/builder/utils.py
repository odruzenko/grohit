from __future__ import annotations
from typing import TYPE_CHECKING
import json

from grafanalib._gen import DashboardEncoder

if TYPE_CHECKING:
    from grafanalib.core import Dashboard as CoreDashboard


def core_dashboard_to_json(core_dashboard: CoreDashboard) -> str:
    return json.dumps(core_dashboard, cls=DashboardEncoder, indent=4)
