"""
API to interact with the parsers
"""

from pathlib import Path

import libcst as cst

from .cst import ExistingListTransformer, NewSettingTransformer


def add_new_value(var_name: str, var_value: str | list[str], file_path: Path):
    """
    Add a new value to the specified setting

    Args:
        var_name (str): The name of the new variable
        var_value (str | list[str]): The value of the variable
        file_path (Path): The path to the file to update
    """
    # read the file
    with file_path.open("r") as f:
        file_content = f.read()

    # parse the file
    module = cst.parse_module(file_content)

    # create the transformer
    transformer = NewSettingTransformer(var_name, var_value)

    # apply the transformer
    updated_module = module.visit(transformer)

    # write the updated file
    with file_path.open("w") as f:
        f.write(updated_module.code)


def update_existing_list(
    var_name: str, var_value: str | list[str], file_path: Path
):
    """
    Update the value of an existing list in the specified setting

    Args:
        var_name (str): The name of the setting to update
        var_value (str | list[str]): The new value of the setting
        file_path (Path): The path to the file to update
    """
    # read the file
    with file_path.open("r") as f:
        file_content = f.read()

    # parse the file content, create transformer, and apply it
    module = cst.parse_module(file_content)
    transformer = ExistingListTransformer(var_name, var_value)
    updated_module = module.visit(transformer)

    # write the updated file
    with file_path.open("w") as f:
        f.write(updated_module.code)
