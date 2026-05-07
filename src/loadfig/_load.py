# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Subparts responsible for loading configuration."""

from __future__ import annotations

import functools
import tomllib
import typing

if typing.TYPE_CHECKING:
    import pathlib


@functools.cache
def toml(path: pathlib.Path) -> dict[typing.Any, typing.Any]:
    """Parse and cache one TOML file.

    __Example:__

    ```python
    import pathlib

    from loadfig import _load

    table = _load.toml(pathlib.Path("pyproject.toml"))
    ```

    Args:
        path:
            TOML file path to parse.

    Returns:
        Decoded TOML table.

    """
    with path.open("rb") as handle:
        return tomllib.load(handle)
