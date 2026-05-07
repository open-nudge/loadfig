# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Test loadfig.pyproject behavior.

Note:
    Most of the functionality is tested through `test_config.py`
    as it uses `loadfig.pyproject` internally.

"""

from __future__ import annotations

import loadfig


def test_none_pyproject() -> None:
    """Test the loading if no `directory` argument is passed."""
    # nosemgrep
    assert "project" in loadfig.pyproject()
