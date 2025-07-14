# SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Load configuration from config (`.<tool>.toml` or `pyproject.toml`)."""

from __future__ import annotations

import pathlib
import tomllib
import typing

from . import _load


def config(
    name: str,
    path: pathlib.Path | str | None = None,
    directory: pathlib.Path | str | None = None,
    vcs: bool = True,  # noqa: FBT001, FBT002
) -> dict[typing.Any, typing.Any]:
    """Read `pyproject.toml` configuration file.

    The following paths are checked in order (first found used):

    - `path` (section `[tool.{name}]` or data in the whole file),
        __if provided__.
    - `.{name}.toml` in the current directory
    - `pyproject.toml` in the current directory
    - `.{name}.toml` in the project root (if `vcs=True`, which is the default)
        as defined by `git`, `hg`, or `svn`
    - `pyproject.toml` in the project root (if `vcs=True`, which is the default)
        as defined by `git`, `hg`, or `svn`

    __Example:__

    Assume the following `pyproject.toml` file at the root of your project:

    ```toml
    [tool.mytool]
    name = "My Tool"
    version = "1.0.0"
    ```

    You can load the configuration for `mytool` using:

    ```python
    import loadfig

    config = loadfig.config("mytool")
    config["name"]  # "My Tool"
    config["version"]  # "1.0.0"
    ```

    > [!IMPORTANT]
    > Automatically returns __only__ the relevant configuration,
    > __not the content of the whole file__.

    > [!WARNING]
    > Empty dictionaries are returned if no configuration was found,
    > client code should handle this case (and have a config with
    > default values to use in such cases).

    Args:
        name:
            The name of the tool to search for in the configuration file.
        path:
            Explicitly provided path to the configuration file, if any.
            If not provided, `loadfig` will try to guess based on `directory`
            and `vcs`.
        directory:
            The directory to search for the configuration file.
            If not provided, the current working directory is used.
        vcs:
            Whether the version control system directories should be
            searched for when localizing the project root (default: `True`).
            Note: This will search for `.git`, `.hg`, or `.svn` directories
            upwards from the `directory` until the root is reached.

    Raises:
        ConfigMissingError:
            If the `path` is specified, but the file does not exist.
        TomlDecodeError:
            If any of the files were found, but could not be read.

    Returns:
        Configuration dictionary of the tool or an empty dictionary
        if no configuration was found.

    """
    if (cfg := _load.specified_path(name, path)) is not None:
        return cfg

    if directory is None:
        directory = pathlib.Path.cwd().resolve()

    files_getters = {
        f".{name}.toml": _file_getter,
        "pyproject.toml": _pyproject_getter,
    }

    for file, getter in files_getters.items():
        path = _load.project_root(file, vcs, start=directory)
        if path is not None:
            with path.open("rb") as handle:
                return getter(tomllib.load(handle), name)

    return {}


def _file_getter(
    dictionary: dict[str, typing.Any], _: str
) -> dict[str, typing.Any]:
    """Get the configuration from a file.

    Args:
        dictionary: The parsed configuration file dictionary.

    Returns:
        The configuration dictionary for the specified tool, or an empty
        dictionary if the tool is not found.

    """
    return dictionary


def _pyproject_getter(
    dictionary: dict[str, typing.Any], name: str
) -> dict[str, typing.Any]:
    """Get the configuration for a specific tool from the `pyproject.toml`.

    Args:
        dictionary: The parsed `pyproject.toml` dictionary.
        name: The name of the tool to search for.

    Returns:
        The configuration dictionary for the specified tool, or an empty
        dictionary if the tool is not found.

    """
    return dictionary.get("tool", {}).get(name, {})
