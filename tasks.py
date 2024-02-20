import json
import pathlib
import sys
from glob import glob
from pathlib import Path

from cookiecutter.main import cookiecutter
from invoke import task


TEMPLATES = ["python"]


@task(help={"template": "Name of the cookiecutter template to test"})
def test(context, template=""):
    """Test a specific cookiecutter template."""
    if not template:
        sys.exit("-t / --template parameter is required!")
    test_dir = pathlib.Path.cwd() / template / "tests"
    if test_dir.exists():
        print(f"Starting Test for {template}")
        context.run(f"pytest { test_dir } -vv --template { template }")
    else:
        sys.exit(f"No Test found for {template}")


@task
def tests(context):
    """Test all available cookiecutter templates.

    First the project specific tests, afterwards global tests.
    """
    for template in TEMPLATES:
        gen_examples(context, template=template)
        test(context, template=template)
    context.run("pytest tests/ -vv")


@task(
    help={
        "build": "Whether to re-bake (build) the example before testing it",
        "example": "Glob-style pattern specifying which baked example(s) to test (default '*')",
        "template": "Name of the cookiecutter template to test",
    }
)
def baked_test(context, build=False, example="*", template=""):
    """Execute tests within a baked cookiecutter example."""
    if not template:
        sys.exit("-t / --template parameter is required!")
    if not glob(f"{template}/examples/{example}"):
        sys.exit(f"No example matching '{example}' found for template '{template}'")
    for baked_cookie in glob(f"{template}/examples/{example}"):
        print(f"Running Tests for {template} example {baked_cookie}")
        with context.cd(baked_cookie):
            # List all of the projects that require a Poetry lock file to be present for the build in this set.
            # This will go ahead and build the lock file as part of the poetry update command for builds to pass.
            if template in (TEMPLATES):
                context.run("poetry update")
            if build:
                context.run("invoke build --no-cache")
            context.run("invoke tests")


@task(help={"template": "Name of the cookiecutter template to update"})
def gen_examples(context, template=""):
    """Update existing examples."""
    if not template:
        sys.exit("-t / --template parameter is required!")
    examples_dir = Path(template).joinpath("examples")
    json_cookie_defaults = Path(template, "cookiecutter_defaults.json")
    data = json.loads(json_cookie_defaults.read_text())

    cookiecutter(
        template=template,
        extra_context=data["cookiecutter"],
        output_dir=str(examples_dir),
        no_input=True,
        overwrite_if_exists=True,
    )
    print(f"\nPlease verify if the {template}/cookiecutter_defaults.json needs to be updated.\n")
