# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Load configuration from config (`.<tool>.toml` or `pyproject.toml`)."""

from __future__ import annotations

import pathlib
import typing

from . import _file, _load, _pyproject  # pyright: ignore[reportPrivateUsage]


def config(
    name: str,
    directory: pathlib.Path | str | None = None,
    vcs: bool = True,  # noqa: FBT001, FBT002
) -> dict[typing.Any, typing.Any]:
    """Read `pyproject.toml` configuration file.

    The following paths are checked in order (first found used):

    - `.{name}.toml` in the current directory
    - `.config/{name}.toml` in the current directory
    - `.{name}.toml` in the project root (if `vcs=True`, which is the default)
    - `.config/{name}.toml` in the project root (if `vcs=True`, which is
    - `pyproject.toml` in the current directory
        as defined by `git`, `hg`, or `svn`
        the default) as defined by `git`, `hg`, or `svn`
    - `pyproject.toml` in the project root (if `vcs=True`, which is the
        default) as defined by `git`, `hg`, or `svn`

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
        directory:
            The directory to search for the configuration file.
            If not provided, the current working directory is used.
        vcs:
            Whether the version control system directories should be
            searched for when localizing the project root (default: `True`).
            Note: This will search for `.git`, `.hg`, or `.svn` directories
            upwards from the `directory` until the root is reached.

    Raises:
        TomlDecodeError:
            If any of the files were found, but could not be read.

    Returns:
        Configuration dictionary of the tool or an empty dictionary
        if no configuration was found.

    """
    if directory is None:
        directory = pathlib.Path.cwd().resolve()

    files = (f".{name}.toml", f".config/{name}.toml")

    for file in files:
        path = _file.find(file, vcs, start=directory)
        if path is not None:
            return _load.toml(path)

    return _pyproject.pyproject(directory, vcs).get("tool", {}).get(name, {})
