"""Rnder a string by jinja2."""

import logging
from typing import Any

from jinja2 import Environment, BaseLoader
from jinja2.exceptions import TemplateSyntaxError


logger = logging.getLogger()


def render_string(template: str, variables: dict[str, Any]):
    """Render a string by jinja2."""
    rendered: str = template
    try:
        temp = Environment(loader=BaseLoader()).from_string(template)
        rendered = temp.render(variables)
    except (TypeError, TemplateSyntaxError) as exception:
        logger.error("String rend failed: %r", exception)
    return rendered
