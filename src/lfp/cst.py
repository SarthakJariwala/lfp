import libcst as cst
from libcst.matchers import Assign, matches


class Transformer(cst.CSTTransformer):
    def __init__(self, setting_to_update: str, apps_to_add: str | list[str]):
        self.setting_to_update = setting_to_update
        self.apps_to_add = (
            apps_to_add if isinstance(apps_to_add, list) else [apps_to_add]
        )

    def _create_new_list_elements(self):
        _len_of_new_items = len(self.apps_to_add)
        _new_elements = []
        for idx, app in enumerate(self.apps_to_add):
            if idx == _len_of_new_items - 1:
                comma = cst.Comma(
                    whitespace_before=cst.SimpleWhitespace(""),
                    whitespace_after=cst.SimpleWhitespace(""),
                )
            else:
                comma = cst.Comma(
                    whitespace_before=cst.SimpleWhitespace(""),
                    # Use ParenthesizedWhitespace for newlines
                    whitespace_after=cst.ParenthesizedWhitespace(
                        first_line=cst.TrailingWhitespace(
                            whitespace=cst.SimpleWhitespace(""),
                            newline=cst.Newline(),
                        ),
                        indent=True,
                        last_line=cst.SimpleWhitespace("    "),
                    ),
                )
            _new_elements.append(
                cst.Element(
                    value=cst.SimpleString(f"'{app}'"),
                    comma=comma,
                )
            )
        return _new_elements

    def leave_Assign(
        self, original_node: cst.Assign, updated_node: cst.Assign
    ) -> cst.Assign:
        if (
            matches(original_node, Assign())
            and original_node.targets[0].target.value == self.setting_to_update
        ):
            # Create new elements list with the additional app
            new_elements = list(updated_node.value.elements)

            # Update the last element to add a comma and newline
            if new_elements:
                last_element = new_elements[-1]
                new_elements[-1] = last_element.with_changes(
                    comma=cst.Comma(
                        whitespace_before=cst.SimpleWhitespace(""),
                        whitespace_after=cst.ParenthesizedWhitespace(
                            first_line=cst.TrailingWhitespace(
                                whitespace=cst.SimpleWhitespace(""),
                                newline=cst.Newline(),
                            ),
                            indent=True,
                            last_line=cst.SimpleWhitespace("    "),
                        ),
                    )
                )

            _new_items = self._create_new_list_elements()
            for new_item in _new_items:
                new_elements.append(new_item)

            return updated_node.with_changes(
                value=updated_node.value.with_changes(elements=new_elements)
            )
        return updated_node


class NewSettingTransformer(cst.CSTTransformer):
    def __init__(self, setting_name: str, setting_value: str | list[str]):
        self.setting_name = setting_name
        self.setting_value = setting_value
        self.setting_exists = False

    def _create_list_elements(self):
        if not isinstance(self.setting_value, list):
            return []

        elements = []
        for idx, value in enumerate(self.setting_value):
            if idx == len(self.setting_value) - 1:
                comma = cst.Comma(
                    whitespace_before=cst.SimpleWhitespace(""),
                    whitespace_after=cst.SimpleWhitespace(""),
                )
            else:
                comma = cst.Comma(
                    whitespace_before=cst.SimpleWhitespace(""),
                    whitespace_after=cst.ParenthesizedWhitespace(
                        first_line=cst.TrailingWhitespace(
                            whitespace=cst.SimpleWhitespace(""),
                            newline=cst.Newline(),
                        ),
                        indent=True,
                        last_line=cst.SimpleWhitespace("    "),
                    ),
                )
            elements.append(
                cst.Element(
                    value=cst.SimpleString(f"'{value}'"),
                    comma=comma,
                )
            )
        return elements

    def _create_value_node(self):
        if isinstance(self.setting_value, list):
            return cst.List(
                elements=self._create_list_elements(),
                lbracket=cst.LeftSquareBracket(
                    whitespace_after=cst.ParenthesizedWhitespace(
                        first_line=cst.TrailingWhitespace(
                            whitespace=cst.SimpleWhitespace(""),
                            newline=cst.Newline(),
                        ),
                        indent=True,
                        last_line=cst.SimpleWhitespace("    "),
                    ),
                ),
                rbracket=cst.RightSquareBracket(
                    whitespace_before=cst.ParenthesizedWhitespace(
                        first_line=cst.TrailingWhitespace(
                            whitespace=cst.SimpleWhitespace(""),
                            newline=cst.Newline(),
                        ),
                    )
                ),
            )
        else:
            # Handle string value
            return cst.SimpleString(f"'{self.setting_value}'")

    def visit_Assign(self, node: cst.Assign) -> bool:
        if node.targets[0].target.value == self.setting_name:
            self.setting_exists = True
        return True

    def leave_Module(
        self, original_node: cst.Module, updated_node: cst.Module
    ) -> cst.Module:
        if not self.setting_exists:
            # Create new assignment node
            new_assignment = cst.SimpleStatementLine(
                body=[
                    cst.Assign(
                        targets=[
                            cst.AssignTarget(target=cst.Name(self.setting_name))
                        ],
                        value=self._create_value_node(),
                    )
                ],
                leading_lines=[
                    cst.EmptyLine(),  # Add blank line before new assignment
                ],
            )

            # Add the new assignment to the module's body
            return updated_node.with_changes(
                body=list(updated_node.body) + [new_assignment]
            )
        return updated_node
