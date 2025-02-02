from pathlib import Path

import pytest

from lfp.parsers.api import add_new_value, update_existing_list


def test_add_new_value_with_string(tmp_path):
    # Create a temporary file with initial content
    test_file = tmp_path / "settings.py"
    initial_content = """
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
]
"""
    test_file.write_text(initial_content)

    # Expected content after modification
    expected_content = """
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
]

NEW_SETTING = 'test_value'
"""

    # Call the function
    add_new_value("NEW_SETTING", "test_value", test_file)

    # Assert the file content matches expected
    assert test_file.read_text() == expected_content


def test_add_new_value_with_list(tmp_path):
    # Create a temporary file with initial content
    test_file = tmp_path / "settings.py"
    initial_content = """
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
]
"""
    test_file.write_text(initial_content)

    # Expected content after modification
    expected_content = """
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
]

NEW_SETTING = [
    'value1',
    'value2',
    'value3',
]
"""

    # Call the function
    add_new_value("NEW_SETTING", ["value1", "value2", "value3"], test_file)

    # Assert the file content matches expected
    assert test_file.read_text() == expected_content


def test_add_new_value_file_not_found():
    # Test with non-existent file
    non_existent_file = Path("/path/does/not/exist.py")

    with pytest.raises(FileNotFoundError):
        add_new_value("NEW_SETTING", "test_value", non_existent_file)


def test_add_new_value_with_single_list_value(tmp_path):
    # Create a temporary file with initial content
    test_file = tmp_path / "settings.py"
    initial_content = """
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
]
"""
    test_file.write_text(initial_content)

    # Expected content after modification
    expected_content = """
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
]

NEW_SETTING = [
    'single_value',
]
"""

    # Call the function
    add_new_value("NEW_SETTING", ["single_value"], test_file)

    # Assert the file content matches expected
    assert test_file.read_text() == expected_content


def test_update_existing_list_with_single_value(tmp_path):
    # Create a temporary file with initial content
    test_file = tmp_path / "settings.py"
    initial_content = """
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
]
"""
    test_file.write_text(initial_content)

    # Expected content after modification
    expected_content = """
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'new_app',
]
"""

    # Call the function
    update_existing_list("INSTALLED_APPS", "new_app", test_file)

    # Assert the file content matches expected
    assert test_file.read_text() == expected_content


def test_update_existing_list_with_multiple_values(tmp_path):
    # Create a temporary file with initial content
    test_file = tmp_path / "settings.py"
    initial_content = """
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
]
"""
    test_file.write_text(initial_content)

    # Expected content after modification
    expected_content = """
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'new_app1',
    'new_app2',
    'new_app3',
]
"""

    # Call the function
    update_existing_list(
        "INSTALLED_APPS", ["new_app1", "new_app2", "new_app3"], test_file
    )

    # Assert the file content matches expected
    assert test_file.read_text() == expected_content


def test_update_existing_list_file_not_found():
    # Test with non-existent file
    non_existent_file = Path("/path/does/not/exist.py")

    with pytest.raises(FileNotFoundError):
        update_existing_list("INSTALLED_APPS", "new_app", non_existent_file)


def test_update_existing_list_with_empty_initial_list(tmp_path):
    # Create a temporary file with initial content
    test_file = tmp_path / "settings.py"
    initial_content = """
INSTALLED_APPS = []
"""
    test_file.write_text(initial_content)

    # Expected content after modification
    expected_content = """
INSTALLED_APPS = ['new_app',]
"""

    # Call the function
    update_existing_list("INSTALLED_APPS", "new_app", test_file)

    # Assert the file content matches expected
    assert test_file.read_text() == expected_content


def test_update_existing_list_multiple_settings(tmp_path):
    # Create a temporary file with multiple settings
    test_file = tmp_path / "settings.py"
    initial_content = """
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
]
"""
    test_file.write_text(initial_content)

    # Expected content after modification
    expected_content = """
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'new_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
]
"""

    # Call the function
    update_existing_list("INSTALLED_APPS", "new_app", test_file)

    # Assert the file content matches expected
    assert test_file.read_text() == expected_content


def test_update_existing_list_preserves_formatting(tmp_path):
    # Create a temporary file with specific formatting
    test_file = tmp_path / "settings.py"
    initial_content = """# This is a comment
INSTALLED_APPS = [
    # Another comment
    'django.contrib.admin',  # Inline comment
    'django.contrib.auth',
]  # End comment
"""
    test_file.write_text(initial_content)

    # Expected content after modification
    expected_content = """# This is a comment
INSTALLED_APPS = [
    # Another comment
    'django.contrib.admin',  # Inline comment
    'django.contrib.auth',
    'new_app',
]  # End comment
"""

    # Call the function
    update_existing_list("INSTALLED_APPS", "new_app", test_file)

    # Assert the file content matches expected
    assert test_file.read_text() == expected_content
