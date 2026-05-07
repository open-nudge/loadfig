<!--
SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
SPDX-FileContributor: szymonmaszke <github@maszke.co>

SPDX-License-Identifier: Apache-2.0
-->

# loadfig

<!-- mkdocs remove start -->

<!-- vale off -->

<!-- pyml disable-num-lines 30 line-length-->

<p align="center">
    <em>One-liner Python pyproject config loader. Lightweight, simple, and VCS-aware with root auto-discovery.</em>
</p>

<div align="center">

<a href="https://pypi.org/project/loadfig">![PyPI - Python Version](https://img.shields.io/pypi/v/loadfig?style=for-the-badge&label=release&labelColor=grey&color=blue)
</a>
<a href="https://pypi.org/project/loadfig">![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fopen-nudge%2Floadfig%2Fmain%2Fpyproject.toml&style=for-the-badge&label=python&labelColor=grey&color=blue)
</a>
<a href="https://opensource.org/licenses/Apache-2.0">![License](https://img.shields.io/badge/License-Apache_2.0-blue?style=for-the-badge)
</a>
<a>![Coverage Hardcoded](https://img.shields.io/badge/coverage-100%25-green?style=for-the-badge)
</a>
<a href="https://scorecard.dev/viewer/?uri=github.com/open-nudge/loadfig">![OSSF-Scorecard Score](https://img.shields.io/ossf-scorecard/github.com/open-nudge/loadfig?style=for-the-badge&label=OSSF)
</a>

</div>

<p align="center">
✨ <a href="#features">Features</a>
🚀 <a href="#quick-start">Quick start</a>
📚 <a href="https://open-nudge.github.io/loadfig">Documentation</a>
🤝 <a href="#contribute">Contribute</a>
👍 <a href="https://github.com/open-nudge/loadfig/blob/main/ADOPTERS.md">Adopters</a>
📜 <a href="#legal">Legal</a>
</p>
<!-- vale on -->

______________________________________________________________________

<!-- mkdocs remove end -->

## Features

__loadfig__ is a Python package designed to load
`pyproject` and `TOML` configuration files adhering to modern standards:

- __Unified__: Load your configuration either from `.<mytool>.toml`,
    `.config/mytool.toml` or `pyproject.toml` (section `[tool.mytool]`)
    using __single line__: `tool_config = loadfig.config(name="<mytool>")`
- __Load `pyproject.toml`__: Find and load the whole `pyproject.toml`
    using single line: `pyproject = loadfig.pyproject()`
- __No dependencies__: Python-only, no third-party dependencies.
- __Do one thing well__: Only load the configuration,
    use other libraries like
    [`python-dotenv`](https://github.com/theskumar/python-dotenv) for bells and whistles.
- __Git-aware__: Automatically detects project's `root` using
    git (or other VCS), no need to specify the path to
    your configuration file.

## Where can I use it?

When creating Python tools and you want to:

- give your users a standard place to configure it
    (`pyproject.toml` or `.<mytool>.toml`)
- make the choices readable and findable
- create tools without maintaining boilerplate

## Quick start

### Installation

```sh
> pip install loadfig
```

### Usage

#### `pyproject.toml` loading

One line is all you need:

```python
# Returns dict with all pyproject contents
pyproject = loadfig.pyproject()

# Get the name of the project
print(pyproject["project"]["name"])
```

#### Tool configuration loading

Assume you have the following section in your `pyproject.toml`
file at the root of your project:

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

That is all you will likely need to do to load your configuration
for your Python project (in a modern, unified way).

> [!IMPORTANT]
> `pyproject.toml` can be located at the root of your project,
> while the loading file can be in a subfolder (e.g. `src/mytool/loader.py`).

See [documentation](https://open-nudge.github.io/loadfig)
for more details about the arguments and options available.

<!-- md-dead-link-check: off -->

<!-- mkdocs remove start -->

## Contribute

We welcome your contributions! Start here:

- [Code of Conduct](/CODE_OF_CONDUCT.md)
- [Contributing Guide](/CONTRIBUTING.md)
- [Roadmap](/ROADMAP.md)
- [Changelog](/CHANGELOG.md)
- [Report security vulnerabilities](/SECURITY.md)
- [Open an Issue](https://github.com/open-nudge/loadfig/issues)

## Legal

- This project is licensed under the _Apache 2.0 License_ - see
    the [LICENSE](/LICENSE.md) file for details.
- This project is copyrighted by _open-nudge_ - the
    appropriate copyright notice is included in each file.

<!-- mkdocs remove end -->

<!-- md-dead-link-check: on -->
