"""Tasks for use with invoke."""
import os
import sys
from distutils.util import strtobool
from pathlib import Path

from invoke import task

try:
    import toml
except ImportError:
    sys.exit("Please make sure to `pip install toml` or enable the Poetry shell and run `poetry install`.")


def is_truthy(arg: str) -> bool:
    """Convert "truthy" strings into Booleans.

    Examples:
        >>> is_truthy('yes')
        True

    Args:
        arg (str): Truthy string (True values are y, yes, t, true, on and 1; false values are n, no,
        f, false, off and 0. Raises ValueError if val is anything else.
    """
    return arg if isinstance(arg, bool) else bool(strtobool(arg))


def python_version(fallback_version: str) -> str:
    """Return the python_version found in the .python-version file or using the provided fallback version.

    Examples:
        >>> python_version('3.11')
        '3.11'

    Args:
        fallback_version (str): python version used as fallback
    """
    try:
        version = Path(".python-version").read_text(encoding="UTF-8").strip()
    except FileNotFoundError:
        version = fallback_version
    return version


FALLBACK_PYVER = "3.11"
PYPROJECT_CONFIG = toml.load("pyproject.toml")
TOOL_CONFIG = PYPROJECT_CONFIG["tool"]["poetry"]

# Can be set to a separate Python version to be used for launching or building image
PYTHON_VER = os.getenv("PYTHON_VER", python_version(FALLBACK_PYVER))
# Name of the docker image/image
IMAGE_NAME = os.getenv("IMAGE_NAME", TOOL_CONFIG["name"])
# Tag for the image
IMAGE_VER = os.getenv("IMAGE_VER", f"{TOOL_CONFIG['version']}-py{PYTHON_VER}")
# Gather current working directory for Docker commands
PWD = os.getcwd()
# Local or Docker execution provide "local" to run locally without docker execution
INVOKE_LOCAL = is_truthy(os.getenv("INVOKE_LOCAL", "no"))  # pylint: disable=W1508


def run_cmd(context, exec_cmd, local=INVOKE_LOCAL):
    """Wrapper to run the invoke task commands.

    Args:
        context ([invoke.task]): Invoke task object.
        exec_cmd ([str]): Command to run.
        local (bool): Define as `True` to execute locally

    Returns:
        result (obj): Contains Invoke result from running task.
    """
    if is_truthy(local):
        print(f"LOCAL - Running command {exec_cmd}")
        return context.run(exec_cmd, pty=True)

    print(f"DOCKER - Running command: {exec_cmd} container: {IMAGE_NAME}:{IMAGE_VER}")
    return context.run(
        f"docker run --rm -it -u $(id -u):$(id -g) -v {PWD}:/local {IMAGE_NAME}:{IMAGE_VER} sh -c '{exec_cmd}'",
        pty=True,
    )


@task(
    help={
        "cache": "Whether to use Docker's cache when building images (default enabled)",
        "force_rm": "Always remove intermediate images",
        "hide": "Suppress output from Docker",
    }
)
def build(context, cache=True, force_rm=False, hide=False):
    """Build a Docker image."""
    print(f"Building image {IMAGE_NAME}:{IMAGE_VER}")
    command = f"docker build --tag {IMAGE_NAME}:{IMAGE_VER} --build-arg PYTHON_VER={PYTHON_VER} -f Dockerfile ."

    if not cache:
        command += " --no-cache"
    if force_rm:
        command += " --force-rm"

    result = context.run(command, hide=hide)
    if result.exited != 0:
        print(f"Failed to build image {IMAGE_NAME}:{IMAGE_VER}\nError: {result.stderr}")


@task
def clean(context):
    """Remove the project specific image."""
    print(f"Attempting to forcefully remove image {IMAGE_NAME}:{IMAGE_VER}")
    context.run(f"docker rmi {IMAGE_NAME}:{IMAGE_VER} --force")
    print(f"Successfully removed image {IMAGE_NAME}:{IMAGE_VER}")


@task
def rebuild(context):
    """Clean the Docker image and then rebuild without using cache."""
    clean(context)
    build(context, cache=False)

# @task()
# def build(context):
#     """Build the project."""
#     print("Building project")
#     command = "poetry build"
#     result = context.run(command)
#     if result.exited != 0:
#         print("Failed to build project")


@task(help={"local": "Run locally or within the Docker container"})
def format(context, local=INVOKE_LOCAL):
    """Format the project."""
    run_cmd(context, "ruff format .", local)
    run_cmd(context, "ruff check --fix", local)


@task(help={"local": "Run locally or within the Docker container"})
def lint(context, local=INVOKE_LOCAL):
    """Lint the project."""
    run_cmd(context, "nox -s lint", local)


@task(help={"local": "Run locally or within the Docker container"})
def test(context, local=INVOKE_LOCAL):
    """Test the project."""
    run_cmd(context, "nox -s tests", local)


@task(help={"local": "Run locally or within the Docker container"})
def mypy(context, local=INVOKE_LOCAL):
    """Run mypy to do type checking."""
    run_cmd(context, "nox -s typing", local)


@task(help={"local": "Run locally or within the Docker container"})
def tests(context, local=INVOKE_LOCAL):
    """Run all tests for this repository."""
    lint(context, local)
    test(context, local)
    mypy(context, local)
    print("All tests have passed!")


@task
def cli(context):
    """Enter the image to perform troubleshooting or dev work."""
    dev = f"docker run -it -v {PWD}:/local {IMAGE_NAME}:{IMAGE_VER} /bin/bash"
    context.run(f"{dev}", pty=True)
