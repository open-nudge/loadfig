# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Functions to work with `pyproject.toml` and other config files."""

from __future__ import annotations

import pathlib


def find(
    file: pathlib.Path | str,
    vcs: bool,  # noqa: FBT001
    start: pathlib.Path | str,
) -> pathlib.Path | None:
    """Find a file in the start directory or a VCS-marked parent.

    > [!IMPORTANT]
    > This function __should not use any third-party libraries__.

    __Example:__

    ```python
    import pathlib

    from loadfig import _file

    path = _file.find("pyproject.toml", vcs=True, start=pathlib.Path.cwd())
    ```

    Args:
        file:
            The file to search for.
        start:
            The starting directory to search from.
        vcs:
            Whether to search for version control system directories.

    Returns:
        Found file path or `None` when no matching file exists.

    """
    start = pathlib.Path(start).resolve()

    if (start / file).is_file():
        return start / file

    if not vcs:
        return None

    vcs_directories = (".git", ".hg", ".svn")

    for path in start.parents:
        for vcs_directory in vcs_directories:
            if (path / vcs_directory).is_dir() and (path / file).is_file():
                return path / file

    return None
