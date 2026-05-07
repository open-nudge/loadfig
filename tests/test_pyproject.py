# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Test loadfig.pyproject behavior.

Note:
    This file contains direct smoke coverage because broader `pyproject()`
    behavior is exercised through config lookup tests.

"""

from __future__ import annotations

import loadfig


def test_none_pyproject() -> None:
    """Assert default-directory pyproject loading returns project metadata."""
    # nosemgrep
    assert "project" in loadfig.pyproject()
