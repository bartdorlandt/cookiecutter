# cookiecutter


- [cookiecutter](#cookiecutter)
  - [Introduction](#introduction)
  - [Prerequisites](#prerequisites)
  - [Why cookiecutter?](#why-cookiecutter)
  - [How To Use Cookiecutter Templates](#how-to-use-cookiecutter-templates)
    - [Using Provided Poetry Environment To Consume Cookiecutter Templates](#using-provided-poetry-environment-to-consume-cookiecutter-templates)
    - [Consuming Cookiecutter Using Git Clone](#consuming-cookiecutter-using-git-clone)
    - [Consuming Cookiecutter Templates via Cookiecutter Commands Without Git Clone](#consuming-cookiecutter-templates-via-cookiecutter-commands-without-git-clone)
    - [Recreating the example cookie](#recreating-the-example-cookie)
  - [Why Poetry?](#why-poetry)
  - [How to use poetry](#how-to-use-poetry)
    - [Adding dependencies to pyproject.toml](#adding-dependencies-to-pyprojecttoml)
    - [Poetry Lock](#poetry-lock)
    - [Poetry Shell](#poetry-shell)
  - [Why Invoke?](#why-invoke)
  - [How To Use Invoke](#how-to-use-invoke)

## Introduction

The intention of this repository is to provide developer environments by making use of [Cookiecutter](https://cookiecutter.readthedocs.io/) template my development standards. There will be situations for deviation, but adhering to these standards is recommended to be able to pick up a project and go with the technologies defined in this repository.

This repository includes the following Cookiecutter templates:

- [python](python/README.md) - template for Python projects

Most projects will take advantage of the following tools: **Cookiecutter**, **Poetry**, **Invoke**, and **Docker Compose**.

## Prerequisites

If you have not already done so, you must have the following already installed.

- [Docker](https://docs.docker.com/get-docker/)
- [Python](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)
- [Cookiecutter](https://cookiecutter.readthedocs.io)

## Why cookiecutter?

Before we get started, let's provide some context around the terminology used within cookiecutter.

- **cookie** - The cookiecutter template that provides the framework for specific projects to allow developers to get started developing faster such as the ones defined [above](#cookiecutter).
- **bake/baking** - The output of a **cookie**. If a **cookie** is baked, it means the project was created from a cookiecutter template.

cookiecutter allows us to codify and package up development standards into a consumable manner that benefits me on quickly getting started with new projects and provides a consistent experience.

cookiecutter uses the concept of a questionnaire and templating to provide logic when building a new project. Let's take a look at one of the existing cookiecutter templates to see the components.

```bash
❯ tree -L 2 python
python
├── README.md
├── cookiecutter.json
├── examples
│   └── baking-contest
├── tests
│   ├── __pycache__
│   └── test_python.py
└── {{cookiecutter.project_slug}}
    ├── Dockerfile
    ├── README.md
    ├── pyproject.toml
    ├── tasks.py
    ├── tests
    └── {{cookiecutter.project_python_name}}
```

You can see that we're able to template folders and the contents of files using similar syntax to Jinja2.

```toml
[tool.poetry]
name = "{{ cookiecutter.project_slug }}"
version = "{{ cookiecutter.version }}"
description = "{{ cookiecutter.description }}"
authors = ["email <email@email.com>"]
```

Within the root of the **python** cookie, we have the **cookiecutter.json** file that provides the questions to a user that is then used in templating.

```json
{
    "codeowner_github_usernames": "@smith",
    "description": "",
    "project_name": "Cookiecutter Project",
    "project_slug": "{{ cookiecutter.project_name.lower().replace(' ', '-').replace('_', '-') }}",
    "project_python_name": "{{ cookiecutter.project_name.lower().replace(' ', '_').replace('-', '_') }}",
    "project_python_base_version": "3.11",
    "project_with_config_settings": ["yes", "no"],
    "generate_docs": ["no", "yes"],
    "version": "1.0.0"
}
```

Here is an example of what it would look like by using just the defaults provided in the **cookiecutter.json** file.

```bash
❯ cookiecutter cookiecutter/python
codeowner_github_usernames [@smith-nda]:
description []:
project_name [Cookiecutter Project]:
project_slug [cookiecutter-project]:
project_python_name [cookiecutter_project]:
project_python_base_version [3.8]:
Select project_with_config_settings:
1 - yes
2 - no
Choose from 1, 2 [1]:
Select generate_docs:
1 - no
2 - yes
Choose from 1, 2 [1]:
version [1.0.0]:

Congratulations!  Your cookie has now been baked. It is located at /home/user/projects/cookiecutter-project.

⚠️⚠️ Before you start using your cookie you must run the following commands inside your cookie:

* poetry lock
* poetry install --with dev --no-root
* poetry shell
```

## How To Use Cookiecutter Templates

> NOTE: cookiecutter is a Python package and can be installed via normal python means.

Cookiecutter must be installed to be able to consume the cookiecutter templates that this repository holds per the [Prerequisites](#prerequisites) above. The link above provides how to install cookiecutter, but we also provide a Poetry virtual environment within this repository.

If you have not used **Poetry** prior to this, it is a Python virtual environment, dependency and packaging manager. Poetry replaces the **requirements.txt** and **setup.py** with a **pyproject.toml** file. Damien (@dgarros) has a great [blog post](https://blog.networktocode.com/post/upgrade-your-python-project-with-poetry/) to get started on using it. Please read [Using Provided Poetry Environment To Consume Cookiecutter Templates](#using-provided-poetry-environment-to-consume-cookiecutter-templates) below.

### Using Provided Poetry Environment To Consume Cookiecutter Templates

1. Clone this repository - `git@github.com:bartdorlandt/cookiecutter.git`
2. Change directory into repository - `cd cookiecutter`
3. Activate the Poetry virtual environment - `poetry shell`

### Consuming Cookiecutter Using Git Clone

> NOTE: Cookiecutter will create the file structure needed within the current working directory unless otherwise specified.

If you followed [Using Provided Poetry Environment To Consume Cookiecutter Templates](#using-provided-poetry-environment-to-consume-cookiecutter-templates) or have the repository cloned already and inside a virtual environment that has cookiecutter installed then follow these directions.

> NOTE: If not freshly cloned, please navigate into the root of the `cookiecutter` and perform a `git pull` to make sure you have the latest updates prior to baking a cookie.

1. If you need to, navigate to where you're not inside the root of this repository, but adjacent to it. If you're within the root of this repository locally, you can also use the `-o` option to specify a directory where you want the baked cookie to be outputted to.

```bash
❯ ls -la
total 32
drwxr-xr-x  23 bart  staff    736 Jun  9 21:16 cookiecutter
```

1. Run `cookiecutter cookiecutter/<template_name>` and answer the cookiecutter prompts to build a specific template. This should output the newly baked cookie into your current working directory.

```bash
❯ ls -la
total 32
drwxr-xr-x  23 bart  staff    736 Jun  9 21:16 cookiecutter
drwxr-xr-x  20 bart  staff    640 Jun  9 22:02 cookiecutter-project
```

### Consuming Cookiecutter Templates via Cookiecutter Commands Without Git Clone

> NOTE: Cookiecutter will create the file structure needed within the current working directory unless otherwise specified.

1. Navigate to the directory where you want the cookie to be outputted to or use the `-o` option to specify the output directory of the baked cookie.

   ```bash
   ❯ ls -la
   total 32
   drwxr-xr-x  23 bart  staff    736 Jun  9 21:16 cookiecutter
   ```

2. Run the following commands depending on your preference.

   - SSH auth: `cookiecutter git@github.com:bartdorlandt/cookiecutter.git --directory <template_name>`
     - Make sure your SSH key is tied to your GitLab account.
     - Answer prompts from Cookiecutter.
   - HTTPS auth: `cookiecutter https://github.com/bartdorlandt/cookiecutter.git --directory <template_name>`
     - This will prompt for credentials.
     - Answer prompts from Cookiecutter.

3. The cookie should now be baked.

   ```bash
   ❯ ls -la
   total 32
   drwxr-xr-x  23 bart  staff    736 Jun  9 21:16 cookiecutter
   drwxr-xr-x  20 bart  staff    640 Jun  9 22:02 cookiecutter-project
   ```

> NOTE: Refer to the template READMEs for specifics on how to use each template.

### Recreating the example cookie
From the root of this project, run the following command and provide the answers to the questions as desired. Using the `python` project as an example:


    cookiecutter  -f -o python/examples python


## Why Poetry?

Poetry was chosen to replace both **requirements.txt** and **setup.py**. Poetry uses the `pyproject.toml` file to define package details, main package dependencies, development dependencies, and tool related configurations. Poetry resolves dependencies and stores the hashes and metadata within the `poetry.lock` file that is then similar to performing a `pip freeze > requirements.txt`, but is more secure due to tracking package hashes. The `poetry.lock` is what is used to provide consistency for package versions across the project to make sure anyone who is developing on it is using the same Python dependency versions. Poetry also provides virtual environments by simply being in the same directory as the `pyproject.toml` and `poetry.lock` files and executing the `poetry shell`.

## How to use poetry

Let's get familiar with the `pyproject.toml` file to understand how to use **Poetry**.

```toml
[tool.poetry]
name = "cookiecutter-project"
version = "1.0.0"
description = ""
authors = ["user <email@email.com>"]
```

The `[tool.poetry]` provides the metadata required for taking advantage of the publishing provided by **Poetry**.

```toml
[tool.poetry.dependencies]
python = "^3.8"
pydantic = {version = "^1.7.2", extras = ["dotenv"]}
toml = "0.10.1"
click = "*"
```

The `[tool.poetry.dependencies]` is where we define our projects main dependencies that will be installed along with it.

```toml
[tool.poetry.dev.dependencies]
pytest = "*"
mock = "*"
requests_mock = "*"
pyyaml = "*"
black = "*"
pylint = "*"
pydocstyle = "*"
yamllint = "*"
bandit = "*"
invoke = "*"
toml = "*"
flake8 = "*"
Sphinx = "*"
myst-parser = "*"
sphinx-autoapi = "*"
sphinx-rtd-theme = "*"
```

The `[tool.poetry.dev.dependencies]` is where we can find development related dependencies. We use this for our testing tools.

```toml
[tool.poetry.group.dev]
optional = true
```

The `[tool.poetry.group.dev]` is where we can set options per group. For the `dev` group the optional flag is set. Therefore not installing it by default.

```toml
[tool.pytest.ini_options]
testpaths = [
    "tests"
]
addopts = "-vv --doctest-modules"
```

Then each tool can provide their own configuration sections that replaces their existing configuration file such as `pytest.ini`.

### Adding dependencies to pyproject.toml

It is rarely a good idea to manage dependencies within `pyproject.toml` by editing the file directly, but instead use the provided `poetry` CLI options.

To add a main dependency, use the `poetry add` command.

> NOTE: To see a few extra examples or available options use `poetry add --help`.

```shell
❯ poetry add sentry-sdk@^1.1.0

Updating dependencies
Resolving dependencies... (1.2s)

Writing lock file

Package operations: 3 installs, 0 updates, 0 removals

  • Installing certifi (2021.5.30)
  • Installing urllib3 (1.26.5)
  • Installing sentry-sdk (1.1.0)
```

If we look at the `pyproject.toml` file, we will see the following line added.

```toml
[tool.poetry.dependencies]

sentry-sdk = "^1.1.0"
```

> NOTE: To understand how to specify dependency constraints, read the [dependency specification](https://python-poetry.org/docs/dependency-specification/) resources provided by **Poetry**.

To add a dependency to a group, for example `dev`, it would be the same command with the `-G <group>` flag

```shell
❯ poetry add sentry-sdk@^1.1.0 -G dev
```

### Poetry Lock

Most of our cookiecutter templates only provide the `pyproject.toml` file and the `poetry.lock` file needs to be generated to be able to use a virtual environment. To generate the `poetry.lock` file is simply running the `poetry lock` command and it will resolve the dependencies and generate the file.

```shell
❯ poetry lock
Updating dependencies
Resolving dependencies... (12.2s)
```

### Poetry Shell

Once the `poetry.lock` file is generated, you can launch the virtual environment using `poetry shell`.

```shell
❯ poetry shell
```

This will get you into a virtual environment, but then you must install the dependencies using the `poetry install` command. By default, this will install all dependencies including development dependencies.

```shell
❯ poetry install
```

You can add `--help` to the `poetry install` command to get more information. To install development dependencies, add `--with=dev`. To not install the local Python package, add `--no-root`.

```shell
❯ poetry install --help

Description:
  Installs the project dependencies.

Usage:
  install [options]

Options:
      --without=WITHOUT   The dependency groups to ignore. (multiple values allowed)
      --with=WITH         The optional dependency groups to include. (multiple values allowed)
      --only=ONLY         The only dependency groups to include. (multiple values allowed)
      --no-dev            Do not install the development dependencies. (Deprecated)
      --sync              Synchronize the environment with the locked packages and the specified groups.
      --no-root           Do not install the root package (the current project).
      --dry-run           Output the operations but do not execute anything (implicitly enables --verbose).
      --remove-untracked  Removes packages not present in the lock file. (Deprecated)
  -E, --extras=EXTRAS     Extra sets of dependencies to install. (multiple values allowed)
      --all-extras        Install all extra dependencies.
      --only-root         Exclude all dependencies.
  -h, --help              Display help for the given command. When no command is given display help for the list command.
  -q, --quiet             Do not output any message.
  -V, --version           Display this application version.
      --ansi              Force ANSI output.
      --no-ansi           Disable ANSI output.
  -n, --no-interaction    Do not ask any interactive question.
      --no-plugins        Disables plugins.
      --no-cache          Disables Poetry source caches.
  -v|vv|vvv, --verbose    Increase the verbosity of messages: 1 for normal output, 2 for more verbose output and 3 for debug.

Help:
  The install command reads the poetry.lock file from
  the current directory, processes it, and downloads and installs all the
  libraries and dependencies outlined in that file. If the file does not
  exist it will look for pyproject.toml and do the same.

  poetry install

  By default, the above command will also install the current project. To install only the
  dependencies and not including the current project, run the command with the
  --no-root option like below:

   poetry install --no-root
```

## Why Invoke?

Invoke is a Python replacement for make. Invoke looks for a `tasks.py` file that contains functions decorated by `@task` that provides the equivalent of a **make target**.

The reason it was chosen over Makefile was due to our collective familiarity with Python and the ability to organize and re-use Invoke tasks across our Cookiecutter templates.

## How To Use Invoke

Invoke is packaged with each Cookiecutter template within the `pyproject.toml` that allows the user to run `poetry shell && poetry install` and have access to the Invoke CLI.

If a `tasks.py` does not exist in the current working directory, the following message will be displayed when attempting to use Invoke.

```shell
❯ invoke
Can't find any collection named 'tasks'!
```

Once in a directory that has a `tasks.py`, you can run `invoke` and see the following output that provides several options for generic Invoke related options.

```shell
❯ invoke
Usage: inv[oke] [--core-opts] task1 [--task1-opts] ... taskN [--taskN-opts]

Core options:

  --complete                         Print tab-completion candidates for given parse remainder.
  --hide=STRING                      Set default value of run()'s 'hide' kwarg.
  --no-dedupe                        Disable task deduplication.
  --print-completion-script=STRING   Print the tab-completion script for your preferred shell (bash|zsh|fish).
  --prompt-for-sudo-password         Prompt user at start of session for the sudo.password config value.
  --write-pyc                        Enable creation of .pyc files.
  -c STRING, --collection=STRING     Specify collection name to load.
  -d, --debug                        Enable debug output.
  -D INT, --list-depth=INT           When listing tasks, only show the first INT levels.
  -e, --echo                         Echo executed commands before running.
  -f STRING, --config=STRING         Runtime configuration file to use.
  -F STRING, --list-format=STRING    Change the display format used when listing tasks. Should be one of: flat (default), nested, json.
  -h [STRING], --help[=STRING]       Show core or per-task help and exit.
  -l [STRING], --list[=STRING]       List available tasks, optionally limited to a namespace.
  -p, --pty                          Use a pty when executing shell commands.
  -r STRING, --search-root=STRING    Change root directory used for finding task modules.
  -R, --dry                          Echo commands instead of running.
  -T INT, --command-timeout=INT      Specify a global command execution timeout, in seconds.
  -V, --version                      Show version and exit.
  -w, --warn-only                    Warn, instead of failing, when shell commands fail.
```

To see what tasks we have available for us to use, we can use the `invoke --list` command.

```shell
❯ invoke --list

Available tasks:

  build     Build a Docker image.
  clean     Remove the project specific image.
  cli       Enter the image to perform troubleshooting or dev work.
  format    Format the project.
  lint      Lint the project.
  mypy      Run mypy to do type checking.
  rebuild   Clean the Docker image and then rebuild without using cache.
  test      Test the project.
  tests     Run all tests for this repository.

```

Each task provides a simple description that helps you determine what it is doing. If you want to get more information on a specific task, use the following command `invoke <task-name> --help`.

```shell
❯ invoke build --help
Usage: inv[oke] [--core-opts] build [--options] [other tasks here ...]

Docstring:
  Build a Docker image.

Options:
  -c, --[no-]cache   Whether to use Docker's cache when building images (default enabled)
  -f, --force-rm     Always remove intermediate images
  -h, --hide         Suppress output from Docker
```
