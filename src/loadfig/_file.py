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
    """Find the project root.

    > [!IMPORTANT]
    > This function __should not use any third-party libraries__.

    Args:
        file:
            The file to search for.
        start:
            The starting directory to search from.
        vcs:
            Whether to search for version control system directories.

    Returns:
        The project root directory.

    """
    start = pathlib.Path(start).resolve()

    if (start / file).is_file():
        return start / file

    if not vcs:
        return None

    vcs_directories = (".git", ".hg", ".svn")

    for path in start.parents:
        for vcs_directory in vcs_directories:
            if (path / vcs_directory).is_dir() and (path / file).exists():
                return path / file

    return None
