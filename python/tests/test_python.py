"""Tests for python cookie to ensure it's working properly."""
import py
import pytest
import json
import re
from pathlib import Path
import jinja2 as j2

# Depending on where the tests are run from
PROJECT = "python"
if Path.cwd().parts[-1] == PROJECT:
    # To allow the tests to be run from within the python dir
    PROJECT = ""

COOKIE = r"{{cookiecutter.project_slug}}"
COOKIE_PATH = Path(PROJECT, COOKIE)
COOKIE_TOML = COOKIE_PATH.joinpath("pyproject.toml")
COOKIE_DEFAULTS_PATH = Path(PROJECT, "cookiecutter_defaults.json")
COOKIE_DEFAULTS = json.loads(COOKIE_DEFAULTS_PATH.read_text())

EXAMPLE_DIRNAME = "baking-contest"
EXAMPLE_PATH = Path(PROJECT, "examples", EXAMPLE_DIRNAME)
EXAMPLE_TOML = EXAMPLE_PATH.joinpath("pyproject.toml")

PYTHON_FILES = [
    Path(".ci", "merge_request.groovy"),
    Path(".ci", "upload_artifactory.groovy"),
    Path(".github", "workflows", "build_and_push.yml"),
    Path(".github", "workflows", "test_code_nox_style.yml"),
    "baking_contest",
    "tests",
    ".dockerignore",
    ".gitignore",
    "Dockerfile",
    "noxfile.py",
    "pyproject.toml",
    "README.md",
    "tasks.py",
]

PYPROJECT = [
    "tool.poetry",
    "tool.poetry.dependencies",
    "tool.poetry.group.dev.dependencies",
    "tool.ruff",
    "tool.ruff.lint",
    "tool.ruff.lint.mccabe",
    "tool.ruff.format",
    "tool.mypy",
    "tool.pytest.ini_options",
]


def get_text_part(toml_text, chapter):
    """Parse the toml file with regex since Jinja makes the toml files non-valid toml files."""
    regex = rf"""(?:\[{chapter}\])(.*?)(?:\n\[\S+\]|\Z)"""
    return re.findall(regex, toml_text, flags=re.S)


def render_j2_string(template_content, context):
    """Render jinja template."""
    j2_tmpl = j2.Template(template_content)
    return j2_tmpl.render(**context)


def init_examples_project(project_name):
    """
    Initialize the examples project folder (by deleting and reconstructing it if
    already created, or just create).

    Args:
        project_name (str): Cookiecutter example project name

    Returns:
        examples_project (py.path.local): Created example project
    """
    # Set examples folder to cookiecutter level directory
    examples_project = py.path.local(f"{__file__}/../../examples/{project_name}")

    # Clean examples project
    if examples_project.isdir():
        examples_project.remove()
    examples_project.mkdir()
    return examples_project


@pytest.fixture
def cookie_defaults():
    """Loads the cookiecutter_defaults.json as an object

    Returns:
        dict: {"cookiecutter": {"key": value, ...}}}
    """
    return json.loads(COOKIE_DEFAULTS_PATH.read_text())


@pytest.fixture
def cookies_baked_project(cookies):
    """
    Sets up an example cookiecutter project

    Args:
        cookies: wrapper for cookiecutter API when generating project

    Return:
        result (cookies.bake): cookies baked project with execution results
        examples_project (py.path.local): created example project
    """
    result = cookies.bake(extra_context={"project_name": "Baking Contest"})

    examples_project = init_examples_project(result.project_path.name)
    result.project_path.replace(examples_project)
    return result, examples_project


@pytest.mark.parametrize("chapter", PYPROJECT)
def test_pyproject_options(chapter, cookie_defaults):
    """Verify that all py project file options are the same."""
    example_toml_txt = EXAMPLE_TOML.read_text()
    base_option = get_text_part(example_toml_txt, chapter)

    cookie_toml_text = COOKIE_TOML.read_text()
    cookie_toml_rendered = render_j2_string(template_content=cookie_toml_text, context=cookie_defaults)
    cookie_option = get_text_part(cookie_toml_rendered, chapter)
    assert base_option == cookie_option, f"Verify that the {chapter} in {EXAMPLE_TOML} is same as in {COOKIE_TOML}."


class TestCookiesBake:
    """Cookiecutter tests for baking."""

    def test_bake_project_success(self, cookies_baked_project):
        """Make sure project bakes successfully."""
        result, examples_project = cookies_baked_project

        assert result.exception is None

        assert result.context["description"] == ""
        assert result.context["project_name"] == "Baking Contest"
        assert result.context["project_slug"] == "baking-contest"
        assert result.context["project_python_name"] == "baking_contest"
        assert result.context["version"] == "1.0.0"

        assert examples_project.isdir()
        assert examples_project.basename == "baking-contest"

        for _file in PYTHON_FILES:
            _path = examples_project.join(_file)
            assert _path.exists()

    # Commenting out for the time being and will work on more thorough testing in the future
    # def test_bake_project_pylint_successful(self, cookies):
    #    """Make sure project passes pylint after creation."""
    #    result = cookies.bake(extra_context={"project_name": "Baking Contest"})

    #    assert result.exception is None

    #    path = Path(result.project_path)
    #    py_files = [str(x) for x in path.rglob("*.py")]

    #    pylint_options = " ".join(py_files)
    #    pylint_stdout, pylint_stderr = lint.py_run(pylint_options, return_std=True)
    #    assert "Your code has been rated at 10.00/10" in pylint_stdout.read()
    #    assert pylint_stderr.read() == ""
