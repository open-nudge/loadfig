# SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Custom exceptions of the `loadfig`."""

from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    import pathlib


class LoadfigError(Exception):
    """Base class for exceptions in this module."""


class ConfigMissingError(LoadfigError):
    """Exception raised when the configuration file is missing."""

    def __init__(self, config: pathlib.Path) -> None:
        """Initialize the exception with the missing configuration file path.

        Args:
            config: The path to the missing configuration file.
        """
        super().__init__(f"Specified configuration file {config} not found.")
