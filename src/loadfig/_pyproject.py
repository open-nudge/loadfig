# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Load `pyproject.toml`."""

from __future__ import annotations

import pathlib
import typing

from . import _file, _load


def pyproject(
    directory: pathlib.Path | str | None = None,
    vcs: bool = True,  # noqa: FBT001, FBT002
) -> dict[typing.Any, typing.Any]:
    """Read `pyproject.toml` configuration file.

    The following paths are checked in order (first found used):

    - `pyproject.toml` in the `directory` (if not specified, `cwd` is used)
    - `pyproject.toml` up the tree if `vcs` is `true`

    Note:
        `pyproject.toml` is loaded once and cached for subsequent usage.

    __Example:__

    Assume the following `pyproject.toml` file at the root of your project:

    ```python
    pyproject = loadfig.pyproject()

    # Get all pyproject dependencies
    pyproject["project"]["dependencies"]
    ```

    Args:
        directory:
            The directory where lookup starts.
            If not provided, the current working directory is used.
        vcs:
            Whether VCS-marked parent directories are considered.
            Note: This searches for `.git`, `.hg`, or `.svn` directories
            upwards from `directory`.

    Raises:
        tomllib.TOMLDecodeError:
            If a found `pyproject.toml` file cannot be decoded.

    Returns:
        `pyproject.toml` content or an empty dictionary
        if no `pyproject.toml` was found.

    """
    if directory is None:
        directory = pathlib.Path.cwd().resolve()

    path = _file.find("pyproject.toml", vcs, start=directory)
    if path is not None:
        return _load.toml(path)

    return {}
