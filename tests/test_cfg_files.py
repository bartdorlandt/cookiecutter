"""Test that the testing configuration files are the same between various cookiecutters."""

import filecmp
import glob
from pathlib import Path
import json
import jinja2 as j2

import pytest

from tasks import TEMPLATES


FILE_CHECKS = [
    ".dockerignore",
    ".gitignore",
]


def read_cookie_json(project_dir):
    """Read example cookiecutter json file."""
    cookie_defaults_json = project_dir.joinpath("cookiecutter_defaults.json")
    return json.loads(cookie_defaults_json.read_text())


@pytest.mark.parametrize("glob_file", FILE_CHECKS)
@pytest.mark.parametrize("template", TEMPLATES)
def test_config_files(glob_file, template):
    """Verify that all configuration files are the same."""
    cfgfiles = glob.glob(f"./{template}/*/{glob_file}")
    cfgfiles.extend(glob.glob(f"./{template}/examples/*/{glob_file}"))
    for cfgfile in cfgfiles[1:]:
        assert filecmp.cmp(cfgfile, cfgfiles[0]) is True, f"Verify that {cfgfile} is same as {cfgfiles[0]}"


# NOTE
# This would replace above test functions as well
# All files are tested with this method
# Non exiting files are skipped, which may be due to options provided
def test_parse_through_jinja():
    """Verify the example data against the cookiecutter source

    Any file in any directory inside the examples directory is verified if it is correctly parsed
    against the source cookiecutter project directory with its current cookiecutter.json data.

    It is expected the .cookiecutter.json file is present in the example project directory.
    This file is used as the data source together with the files, they are parsed through jinja and validated.

    Non existing files are skipped, it is assumed those are conditionally present.
    """
    # Setting the env extension to be able to cope with 'now': "{% now 'local', '%Y' %}"
    env = j2.Environment(extensions=["jinja2_time.TimeExtension"])

    base_path = Path()
    project_dirs = base_path.rglob("cookiecutter.json")
    for project_dir_path in project_dirs:
        project_dir = project_dir_path.parent
        # Expecting only a single cookiecutter template directory
        cc_dir = next(project_dir.glob(r"{{cookiecutter*"))
        cc_files = cc_dir.rglob("*")

        for example_project_dir in project_dir.joinpath("examples").glob("*"):
            for cc_file in cc_files:
                if cc_file.is_dir():
                    continue
                template_file = Path(*cc_file.parts[2:])
                cookie_file = example_project_dir.joinpath(template_file)
                if not cookie_file.exists():
                    # print(f"File {cookie_file} was not created, skipping.")
                    continue

                j2_tpl = env.from_string(cc_file.read_text())
                cookie_data = read_cookie_json(project_dir)
                baked_tpl = j2_tpl.render(cookie_data).rstrip("\n")
                cookie_txt = cookie_file.read_text().rstrip("\n")
                assert (
                    baked_tpl == cookie_txt
                ), f"The example file doesn't match the parsed source. {cc_file} != {cookie_file}"
