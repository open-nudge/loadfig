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
    """Cached TOML loading.

    Args:
        path:
            The path from which to load the file

    Returns:
        Dictionary with TOML content

    """
    with path.open("rb") as handle:
        return tomllib.load(handle)
