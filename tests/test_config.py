# SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Test loadfig.config.

Tests are ran across multiple nested directory levels:

- Bottom level directory with all files
(should be preferred if this is where we start the search)
- Middle level directory with no files
(should be skipped in favor of the top level directory if
this is where we start the search)
- Top level directory with all files (should be preferred
if this is where we start the search OR if vcs=True)

Whole structure is created in a temporary directory via module-wide
fixture and removed afterwards.

"""

from __future__ import annotations

import shutil
import typing

import tomli_w

import pytest

import loadfig

if typing.TYPE_CHECKING:
    import pathlib

    from collections.abc import Iterator

BOTTOM = 0
MIDDLE = 1
TOP = -1

NONEXISTENT = "nfeaknfkwakgnksagmkgsm"
CONFIG = "config"
HIDDEN = "hidden"
SPECIFIED = "specified"

PYPROJECT_FILENAME = "pyproject.toml"

# Type aliases
DIRECTORY_PLACEMENT = typing.Literal[0, 1, -1]


@pytest.fixture(scope="module", autouse=True)
def paths(
    tmp_path_factory: pytest.TempPathFactory,
) -> Iterator[list[pathlib.Path]]:
    """Create a temporary nested directory structure for testing.

    Args:
        tmp_path_factory:
            Pytest fixture for creating temporary directories

    Yields:
        List of paths to the directory created. Each path
        corresponds to a different directory level in the
        nested structure.
    """
    top = tmp_path_factory.mktemp("top")
    # Bottom, middle, top, tmpdir
    path = top / "middle" / "bottom"
    path.mkdir(parents=True)
    paths = list(path.parents)[:3]  # Exclude /

    # Top level directory, which can be searched for
    _create_subdir(paths[TOP], has_vcs=True)
    # Bottom level which should be a priority
    # IF we are in the bottom level directory
    # Otherwise it should be ignored
    _create_subdir(paths[BOTTOM], has_vcs=False)

    yield paths

    shutil.rmtree(top)


@pytest.mark.parametrize("name", (CONFIG, HIDDEN, NONEXISTENT))
@pytest.mark.parametrize("directory_placement", (BOTTOM, MIDDLE, TOP))
@pytest.mark.parametrize("vcs", (False, True))
def test_autoload(
    name: str,
    directory_placement: DIRECTORY_PLACEMENT,
    vcs: bool,  # noqa: FBT001
    paths: list[pathlib.Path],
) -> None:
    """Test the `loadfig.config` function with no path specified.

    Args:
        name:
            Name of the configuration file to search for
        directory_placement:
            Directory level to start the search from
        vcs:
            Whether the directory has a VCS directory
        paths:
            List of paths to the directories created for testing
    """
    result = {"correct": True, "has_vcs": True}

    # Bottom level directory should be prioritized which has no git simulation
    if directory_placement == BOTTOM:
        result["has_vcs"] = False
    # Config could not be found automatically, therefore empty dict
    if (directory_placement == MIDDLE and not vcs) or name == NONEXISTENT:
        result = {}

    assert (
        loadfig.config(name, directory=paths[directory_placement], vcs=vcs)
        == result
    )


@pytest.mark.parametrize("vcs", (False, True))
@pytest.mark.parametrize("name", (CONFIG, NONEXISTENT))
@pytest.mark.parametrize("directory_placement", (BOTTOM, TOP))
@pytest.mark.parametrize("filename", (PYPROJECT_FILENAME, f"{SPECIFIED}.toml"))
def test_correct_path(
    name: str,
    directory_placement: DIRECTORY_PLACEMENT,
    filename: str,
    vcs: bool,  # noqa: FBT001
    paths: list[pathlib.Path],
) -> None:
    """Test the `loadfig.config` function with a specified path.

    Args:
        name:
            Name of the configuration file to search for
        directory_placement:
            Directory level to start the search from
        filename:
            Name of the file to search for
        vcs:
            Whether the directory has a VCS directory
            (should not affect the tests)
        paths:
            List of paths to the directories created for testing
    """
    if filename == PYPROJECT_FILENAME and name == NONEXISTENT:
        assert (
            len(
                loadfig.config(
                    name, path=paths[directory_placement] / filename, vcs=vcs
                )
            )
            == 0
        )
    else:
        assert loadfig.config(
            name, path=paths[directory_placement] / filename, vcs=vcs
        )["correct"]


@pytest.mark.parametrize("directory_placement", (BOTTOM, TOP))
def test_wrong_path(
    directory_placement: DIRECTORY_PLACEMENT,
    paths: list[pathlib.Path],
) -> None:
    """Test what happens when the provided path is wrong.

    Args:
        directory_placement (typing.Literal[BOTTOM, MIDDLE, TOP]):
            Directory level to start the search from, should
            not matter as the path is incorrect.
        paths:
            List of paths to the directories created for testing
    """
    with pytest.raises(loadfig.error.ConfigMissingError):
        _ = loadfig.config(
            name="does_not_matter",
            path="whatever/this/does/not/exist",
            directory=paths[directory_placement],
        )


def test_no_directory() -> None:
    """Test default directory behavior when no directory is provided.

    This project's `pyproject.toml` should be loaded in such case.

    """
    assert len(loadfig.config(name="does_not_matter")) == 0


##############################################################################
#
#                           HELPER FUNCTIONS
#
##############################################################################


def _save_toml(path: pathlib.Path, data: dict[typing.Any, typing.Any]) -> None:
    """Save a dictionary to a TOML file.

    Args:
        path:
            Path to the file
        data:
            Dictionary to save

    """
    with path.open("wb") as handle:
        tomli_w.dump(data, handle)


def _create_subdir(
    path: pathlib.Path,
    has_vcs: bool,  # noqa: FBT001
) -> None:
    """Create a directory with all TOML config files.

    Allows for testing of the `loadfig.config` function
    across many different configuration files
    __at a specific directory level__.

    Args:
        path:
            Directory path to create
        has_vcs:
            Whether to create a `.git` directory
            (to simulate a VCS directory)

    """
    if has_vcs:
        (path / ".git").mkdir()

    data = {
        path / "pyproject.toml": {
            "tool": {
                CONFIG: {"correct": True, "has_vcs": has_vcs},
                HIDDEN: {"correct": False, "has_vcs": has_vcs},
                SPECIFIED: {"correct": False, "has_vcs": has_vcs},
            },
        },
        # Has priority over the pyproject.toml
        path / f".{HIDDEN}.toml": {"correct": True, "has_vcs": has_vcs},
        # Has priority over .{SPECIFIED}.toml as it is explicitly specified
        path / f"{SPECIFIED}.toml": {"correct": True, "has_vcs": has_vcs},
        path / f".{SPECIFIED}.toml": {"correct": False, "has_vcs": has_vcs},
    }

    for subpath, config in data.items():
        _save_toml(subpath, config)
