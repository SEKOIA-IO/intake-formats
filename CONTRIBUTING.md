# Contributing

Thanks for being interested in contributing to Sekoia.io intake formats. This document describes how to contribute to this repository.

## Prerequisites

To contribute to this repository, you will need the following development setup:

- A Github account

  To fork the repository and create pull requests

- [Git](https://git-scm.com/)

  To pull the repository and push your changes

- Python3

  We recommend you to use Python3.10 or higher.
  To ease python version management, you can use [pyenv](https://github.com/pyenv/pyenv#installation).

- [Poetry](https://python-poetry.org/docs/#installation)

  To execute helper scripts in the directory `utils/`

## How to contribute

- [Fork](https://github.com/SEKOIA-IO/intake-formats/fork) the repository
- Clone the repository in local with `git clone https://github.com/<my-account>/intake-formats.git .`
- Create or modify a format. See our [documentation](#documentation) to understand how to develop a new format.
- Test your changes. See [testing](doc/testing.md) to see how to verify your changes.
- Lint your files using `npx prettier --write <your files>` or `npx prettier --write .` at the root of the repository ([How to install `Prettier`](https://prettier.io/docs/en/install.html))
- Push your changes and create a [pull request](https://github.com/SEKOIA-IO/intake-formats/compare)

## <a id="documentation"></a> Documentation

To understand how to develop a new format, refer to our [documentation](doc/README.md).

## Contribution CheckList

To ensure the quality of contribution, the following points will be reviewed in your changes:

- Have clear descriptions for new modules, new formats and taxonomy.
- A logo is provided for any new modules and any new formats.
- Tests should cover at least 75% of parsers.
- At least one smart-description is provide for any new format.
