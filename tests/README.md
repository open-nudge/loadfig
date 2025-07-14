<!--
SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
SPDX-FileContributor: szymonmaszke <github@maszke.co>

SPDX-License-Identifier: Apache-2.0
-->

# Tests of loadfig

- `test_smoke.py` - generic
    [smoke tests](https://grafana.com/blog/2024/01/30/smoke-testing/)
    to check if the package is importable
- `test_config.py` - test core config loading

## Core config loading

Tests are relatively complex, as these units tests are run across matrix.
Please refer to the docstrings of specific tests for more details.
