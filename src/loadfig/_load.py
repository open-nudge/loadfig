# SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Subparts responsible for loading configuration."""

from __future__ import annotations

import pathlib
import tomllib
import typing

from . import error


def specified_path(
    name: str,
    path: pathlib.Path | str | None,
) -> dict[typing.Any, typing.Any] | None:
    """Load configuration from the specified path.

    Args:
        name:
            The name of the tool to search for in the configuration file.
        path:
            Explicitly provided path to the configuration file, if any.

    Raises:
        ConfigMissingError:
            If the `path` is specified, but the file does not exist.
        TomlDecodeError:
            If the file was found, but could not be read.

    Returns:
        Configuration dictionary of the tool or `None`.

    """
    if path is None:
        return None

    path = pathlib.Path(path)
    if not path.exists():
        raise error.ConfigMissingError(path)

    with path.open("rb") as handle:
        data = tomllib.load(handle)

    if "tool" in data:
        return data["tool"].get(name, {})

    return data


def project_root(
    file: pathlib.Path | str,
    vcs: bool,  # noqa: FBT001
    start: pathlib.Path | str,
) -> pathlib.Path | None:
    """Find the project root.

    > [!IMPORTANT]
    > This function __should not use any third-party libraries__.

    Args:
        file: The file to search for.
        start: The starting directory to search from.
        vcs: Whether to search for version control system directories.

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
