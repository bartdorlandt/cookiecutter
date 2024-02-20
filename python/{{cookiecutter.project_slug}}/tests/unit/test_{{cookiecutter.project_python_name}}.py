
#!/usr/bin/env python3
"""{{ cookiecutter.project_python_name }} script."""
from {{ cookiecutter.project_python_name }} import {{ cookiecutter.project_python_name }} as src


def test_create_container():
    """Test create_container."""
    name = "test"
    email = "test@test.com"
    container = src.create_container(name, email)
    assert container.name == name
    assert container.email == email
    assert container.extra == ""


def test_create_container2():
    """Test create_container."""
    name = "test"
    email = "test@test.com"
    extra = "another test"
    container = src.create_container(name, email, extra)
    assert container.name == name
    assert container.email == email
    assert container.extra == ""

