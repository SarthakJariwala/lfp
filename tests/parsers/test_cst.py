import libcst as cst

from lfp.parsers.cst import ExistingListTransformer, NewSettingTransformer


def test_addition_to_list():
    sample = """
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
]

OTHER_LIST = [
    'item1',
    'item2',
]
"""

    expected = """
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'mynewapp',
    'anotherapp',
]

OTHER_LIST = [
    'item1',
    'item2',
]
"""

    # Parse the code into a CST
    module = cst.parse_module(sample)

    # Apply the transformer
    transformed_module = module.visit(
        ExistingListTransformer(
            var_name="INSTALLED_APPS",
            var_value=["mynewapp", "anotherapp"],
        )
    )

    # Print the modified code
    assert transformed_module.code == expected


def test_new_setting_addition_with_list_value():
    sample = """
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
]

OTHER_LIST = [
    'item1',
    'item2',
]
"""

    expected = """
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
]

OTHER_LIST = [
    'item1',
    'item2',
]

MY_SETTING = [
    'value1',
    'value2',
    'value3',
]
"""

    # Parse the code into a CST
    module = cst.parse_module(sample)

    # Apply the transformer
    transformed_module = module.visit(
        NewSettingTransformer(
            var_name="MY_SETTING",
            var_value=["value1", "value2", "value3"],
        )
    )
    assert transformed_module.code == expected


def test_new_setting_addition_with_single_list_value():
    sample = """
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
]

OTHER_LIST = [
    'item1',
    'item2',
]
"""

    expected = """
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
]

OTHER_LIST = [
    'item1',
    'item2',
]

MY_SETTING = [
    'value1',
]
"""

    # Parse the code into a CST
    module = cst.parse_module(sample)

    # Apply the transformer
    transformed_module = module.visit(
        NewSettingTransformer(
            var_name="MY_SETTING",
            var_value=["value1"],
        )
    )

    assert transformed_module.code == expected


def test_new_setting_addition_with_string_value():
    sample = """
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
]

OTHER_LIST = [
    'item1',
    'item2',
]
"""

    expected = """
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
]

OTHER_LIST = [
    'item1',
    'item2',
]

MY_SETTING = 'value1'
"""

    # Parse the code into a CST
    module = cst.parse_module(sample)

    # Apply the transformer
    transformed_module = module.visit(
        NewSettingTransformer(
            var_name="MY_SETTING",
            var_value="value1",
        )
    )

    assert transformed_module.code == expected
