# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Test loadfig.config lookup behavior."""

from __future__ import annotations

import typing

import tomli_w

import pytest

import loadfig

if typing.TYPE_CHECKING:
    import pathlib


@pytest.fixture(scope="module")
def paths(tmp_path_factory: pytest.TempPathFactory) -> dict[str, pathlib.Path]:
    """Create nested directories used by config lookup tests.

    Args:
        tmp_path_factory:
            Pytest factory creating the temporary top directory.

    Returns:
        Named directory paths for top, middle, and bottom levels.

    """
    top = tmp_path_factory.mktemp("top").resolve()
    middle = (top / "middle").resolve()
    bottom = (middle / "bottom").resolve()
    bottom.mkdir(parents=True)

    _create_subdir(top, "top", has_vcs=True)
    _create_subdir(bottom, "bottom", has_vcs=False)

    return {"bottom": bottom, "middle": middle, "top": top}


@pytest.mark.parametrize(
    ("name", "start", "vcs", "expected"),
    (
        pytest.param(
            "config",
            "bottom",
            False,
            {"correct": True, "has_vcs": False, "level": "bottom"},
            id="config-bottom-no-vcs",
        ),
        pytest.param(
            "config",
            "bottom",
            True,
            {"correct": True, "has_vcs": False, "level": "bottom"},
            id="config-bottom-vcs",
        ),
        pytest.param("config", "middle", False, {}, id="config-middle-no-vcs"),
        pytest.param(
            "config",
            "middle",
            True,
            {"correct": True, "has_vcs": True, "level": "top"},
            id="config-middle-vcs",
        ),
        pytest.param(
            "config",
            "top",
            False,
            {"correct": True, "has_vcs": True, "level": "top"},
            id="config-top-no-vcs",
        ),
        pytest.param(
            "config",
            "top",
            True,
            {"correct": True, "has_vcs": True, "level": "top"},
            id="config-top-vcs",
        ),
        pytest.param(
            "hidden",
            "bottom",
            False,
            {"correct": True, "has_vcs": False, "level": "bottom"},
            id="hidden-bottom-no-vcs",
        ),
        pytest.param(
            "hidden",
            "bottom",
            True,
            {"correct": True, "has_vcs": False, "level": "bottom"},
            id="hidden-bottom-vcs",
        ),
        pytest.param("hidden", "middle", False, {}, id="hidden-middle-no-vcs"),
        pytest.param(
            "hidden",
            "middle",
            True,
            {"correct": True, "has_vcs": True, "level": "top"},
            id="hidden-middle-vcs",
        ),
        pytest.param(
            "hidden",
            "top",
            False,
            {"correct": True, "has_vcs": True, "level": "top"},
            id="hidden-top-no-vcs",
        ),
        pytest.param(
            "hidden",
            "top",
            True,
            {"correct": True, "has_vcs": True, "level": "top"},
            id="hidden-top-vcs",
        ),
        pytest.param(
            "nonexistent",
            "bottom",
            False,
            {},
            id="nonexistent-bottom-no-vcs",
        ),
        pytest.param(
            "nonexistent",
            "bottom",
            True,
            {},
            id="nonexistent-bottom-vcs",
        ),
        pytest.param(
            "nonexistent",
            "middle",
            False,
            {},
            id="nonexistent-middle-no-vcs",
        ),
        pytest.param(
            "nonexistent",
            "middle",
            True,
            {},
            id="nonexistent-middle-vcs",
        ),
        pytest.param(
            "nonexistent",
            "top",
            False,
            {},
            id="nonexistent-top-no-vcs",
        ),
        pytest.param(
            "nonexistent",
            "top",
            True,
            {},
            id="nonexistent-top-vcs",
        ),
    ),
)
def test_autoload(
    name: str,
    start: str,
    # enq: Parametrized booleans are the behavior surface under test.
    vcs: bool,  # noqa: FBT001
    expected: dict[typing.Any, typing.Any],
    paths: dict[str, pathlib.Path],
) -> None:
    """Test automatic config lookup across levels and VCS modes.

    Args:
        name:
            Configuration name passed to `loadfig.config`.
        start:
            Directory level where lookup starts.
        vcs:
            Whether parent VCS lookup is enabled.
        expected:
            Configuration expected from the lookup.
        paths:
            Named directory paths created for this module.

    """
    # nosemgrep
    assert loadfig.config(name, directory=paths[start], vcs=vcs) == expected


def test_none_directory() -> None:
    """Test the loading if no `directory` argument is passed on dummy tool."""
    # nosemgrep
    assert loadfig.config("non-existent-very-unlikely-tool") == {}


def test_config_fallback(tmp_path: pathlib.Path) -> None:
    """Test lookup through the documented `.config/{name}.toml` path.

    Args:
        tmp_path:
            Temporary directory used as the config lookup root.

    """
    root = tmp_path.resolve()
    path = (root / ".config" / "fallback.toml").resolve()
    path.parent.mkdir()
    _save_toml(path, {"correct": True})

    # nosemgrep
    assert loadfig.config("fallback", directory=root, vcs=False) == {
        "correct": True,
    }


def _save_toml(path: pathlib.Path, data: dict[typing.Any, typing.Any]) -> None:
    """Save TOML data to a path.

    Args:
        path:
            TOML file path to write.
        data:
            Mapping serialized into the TOML file.

    """
    with path.open("wb") as handle:
        tomli_w.dump(data, handle)


def _create_subdir(
    path: pathlib.Path,
    level: str,
    # enq: Fixture setup mirrors VCS and non-VCS directories explicitly.
    has_vcs: bool,  # noqa: FBT001
) -> None:
    """Create config files for one lookup level.

    Args:
        path:
            Directory receiving config files.
        level:
            Human-readable directory level stored in fixture data.
        has_vcs:
            Whether to create a `.git` marker in the directory.

    """
    if has_vcs:
        (path / ".git").mkdir()

    values = {"correct": True, "has_vcs": has_vcs, "level": level}
    data = {
        path / "pyproject.toml": {
            "tool": {
                "config": values,
                "hidden": {
                    "correct": False,
                    "has_vcs": has_vcs,
                    "level": level,
                },
            },
        },
        path / ".hidden.toml": values,
    }

    for subpath, config in data.items():
        _save_toml(subpath.resolve(), config)
