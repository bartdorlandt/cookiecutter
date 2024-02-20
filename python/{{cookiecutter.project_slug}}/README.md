# Introduction
{{ cookiecutter.description }}

### Local installation
The dependencies are managed by [poetry](https://python-poetry.org/).

    poetry config virtualenvs.in-project true
    poetry install --with dev --no-root
    poetry shell

### Using docker
A tasks.py file is provided which can be used by `invoke`. This is installed with the local installation steps.

To build the docker container:

    inv build

To clean (remove) the docker container and image:

    inv clean

A shorthand to rebuild the container:

    inv rebuild

### Commands
Commands can be executed on the code, like linting, testing and formatting. All the commands will by default be executed in a docker. The `-l` flag can be provided to run them locally.

    inv format
    inv lint
    inv test
    inv mypy

To view all available options:

    inv -l
