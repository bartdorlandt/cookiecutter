#!/usr/bin/env python3
"""{{cookiecutter.project_python_name}} script."""
import typing
from dataclasses import dataclass


@dataclass
class Container:
    """Container dataclass."""

    name: str
    email: str
    extra: str = ""


ContainerInfo: typing.TypeAlias = dict[str, Container]


def example(container: ContainerInfo) -> None:
    """Print the content of the Contairers."""
    for name, info in container.items():
        print(f"Name: {name}, Email: {info.email}, Extra: {info.extra}")


def create_container(name: str, email: str, extra: str = "") -> Container:
    """Create a container."""
    return Container(name, email, extra)
