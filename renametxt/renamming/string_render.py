"""Rnder a string by jinja2."""

import logging
from typing import Any

from rich.logging import RichHandler
from jinja2 import Environment, BaseLoader


logging.basicConfig(level=logging.DEBUG, format="%(message)s", handlers=(RichHandler(), ))
log = logging.getLogger()


def string_render(template: str, variables: dict[str, Any]):
    """Rnder a string by jinja2."""
    rendered: str = template
    try:
        temp = Environment(loader=BaseLoader).from_string(template)  # type: ignore
        rendered = temp.render(variables)
    except TypeError as exception:
        log.error("String rend failed: %r", exception)
    return rendered
