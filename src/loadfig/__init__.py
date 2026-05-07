# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

# pyright: reportImportCycles=false

"""Official `loadfig` documentation.

Minimalistic library for loading tool-specific configuration from
configuration files (either `.<tool>.toml` or `pyproject.toml`).

"""

from __future__ import annotations

from importlib.metadata import version

from ._config import config
from ._pyproject import pyproject

__version__ = version("loadfig")
"""Current loadfig version."""

del version

__all__: list[str] = [
    "__version__",
    "config",
    "pyproject",
]
