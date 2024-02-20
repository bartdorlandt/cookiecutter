"""noxfile."""
from nox_poetry import session as nox_session

py_versions = ["{{ cookiecutter.project_python_base_version }}"]


@nox_session(python=py_versions[0])
def lint(session):
    """Lint the project."""
    session.install("ruff")
    session.run("ruff", "format", "--check")
    session.run("ruff", "check", ".")


@nox_session(python=py_versions)
def tests(session):
    """Test the project."""
    # session.run("poetry", "install", "--with", "dev", external=True)
    session.run("poetry", "install", "--with", "dev")
    session.run("pytest", *session.posargs)


@nox_session(python=py_versions[0])
def typing(session):
    """Type check the project."""
    session.install("mypy")
    session.run("mypy", ".", "--junit-xml", "mypy_report.xml")
