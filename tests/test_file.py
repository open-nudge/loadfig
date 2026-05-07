# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Test low-level file discovery."""

from __future__ import annotations

import typing

from loadfig import _file

if typing.TYPE_CHECKING:
    import pathlib


def test_find_local(tmp_path: pathlib.Path) -> None:
    """Test that a relative local file is found in the start directory.

    Args:
        tmp_path:
            Temporary directory used as the lookup root.
    """
    start = tmp_path.resolve()
    path = (start / "settings.toml").resolve()
    path.touch()

    # nosemgrep
    assert _file.find("settings.toml", vcs=False, start=start) == path


def test_parent_vcs(tmp_path: pathlib.Path) -> None:
    """Test that a parent file is found when VCS lookup is enabled.

    Args:
        tmp_path:
            Temporary directory used as the lookup root.
    """
    root = tmp_path.resolve()
    start = _create_nested(root)
    path = (root / "settings.toml").resolve()
    path.touch()
    (root / ".git").mkdir()

    # nosemgrep
    assert _file.find("settings.toml", vcs=True, start=start) == path


def test_parent_false(tmp_path: pathlib.Path) -> None:
    """Test that a parent file is ignored when VCS lookup is disabled.

    Args:
        tmp_path:
            Temporary directory used as the lookup root.
    """
    root = tmp_path.resolve()
    start = _create_nested(root)
    (root / "settings.toml").resolve().touch()
    (root / ".git").mkdir()

    # nosemgrep
    assert _file.find("settings.toml", vcs=False, start=start) is None


def test_parent_marker(tmp_path: pathlib.Path) -> None:
    """Test that a parent file is ignored without a VCS marker.

    Args:
        tmp_path:
            Temporary directory used as the lookup root.
    """
    root = tmp_path.resolve()
    start = _create_nested(root)
    (root / "settings.toml").resolve().touch()

    # nosemgrep
    assert _file.find("settings.toml", vcs=True, start=start) is None


def _create_nested(path: pathlib.Path) -> pathlib.Path:
    """Create and return a nested lookup start directory.

    Args:
        path:
            Root directory under which nested folders are created.

    Returns:
        Resolved bottom-level directory used as lookup start.
    """
    start = (path / "middle" / "bottom").resolve()
    start.mkdir(parents=True)
    return start
