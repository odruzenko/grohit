from __future__ import annotations

import pytest
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tests.types import FixtureDirGetter


@pytest.fixture(scope="session")
def fixture_base() -> Path:
    return Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def fixture_dir(fixture_base: Path) -> FixtureDirGetter:
    def _fixture_dir(name: str) -> Path:
        return fixture_base / name

    return _fixture_dir
