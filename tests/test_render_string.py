# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import unittest
from typing import Any
from dataclasses import dataclass
from render_renamer.renaming.render_string import render_string


class TestRenderString(unittest.TestCase):
    def test_render_string(self) -> None:
        @dataclass
        class TestCase:
            template: str
            variables: dict[str, Any]
            expected: str

        cases = [
            TestCase(
                "Hello, {{ name }}!",
                {"name": "World"},
                "Hello, World!"
            ),
            TestCase(
                "Sum: {{ a + b }}",
                {"a": 5, "b": 3},
                "Sum: 8"
            ),
            TestCase(
                "Items: {% for item in items %}{{ item }} {% endfor %}",
                {"items": ["apple", "banana", "cherry"]},
                "Items: apple banana cherry "
            ),
            TestCase(
                "No variables here.",
                {},
                "No variables here."
            ),
            TestCase(
                "{{ not_a_variable }}",
                {},
                ""
            ),
            TestCase(
                "{% if condition %}True{% else %}False{% endif %}",
                {"condition": True},
                "True"
            ),
            TestCase(
                "{% if condition %}True{% else %}False{% endif %}",
                {"condition": False},
                "False"
            ),
            TestCase(
                "Nested: {{ outer }} and {{ inner }}",
                {"outer": "Out", "inner": "In"},
                "Nested: Out and In"
            ),
            TestCase(
                "Math: {{ (x * y) + z }}",
                {"x": 2, "y": 3, "z": 4},
                "Math: 10"
            ),
            TestCase(
                "List length: {{ items|length }}",
                {"items": [1, 2, 3, 4]},
                "List length: 4"
            ),
            TestCase(
                "invalid {{ syntax ",
                {},
                "invalid {{ syntax "
            ),
        ]

        for case in cases:
            self.assertEqual(
                render_string(case.template, case.variables),
                case.expected
            )
