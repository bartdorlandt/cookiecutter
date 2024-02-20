"""Used to setup fixtures to be used through tests."""
# import sys
import pytest
from click.testing import CliRunner

# sys.path.append("{{ cookiecutter.project_python_name }}/some_path")


@pytest.fixture
def cli_runner():
    """Provide CLI runner for Click tests."""
    return CliRunner()


@pytest.fixture
def sample_fixture():
    """Provide <sample> for tests."""
    return "some test input"
