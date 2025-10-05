"""
Return a Rich Text object showing the differences between two strings.
"""

from difflib import SequenceMatcher
from rich.text import Text
from rich.theme import Theme


def rich_difference_strings(src: str, dst: str) -> Text:
    """
    Return a Rich Text object showing the differences between two strings.
    """
    sequence_matcher = SequenceMatcher(None, src, dst)
    text = Text()
    for tag, i1, i2, j1, j2 in sequence_matcher.get_opcodes():
        match tag:
            case "equal":
                text.append(src[i1:i2], style="equal")
            case "replace":
                text.append(src[i1:i2], style="replaced")
                text.append(dst[j1:j2], style="replacing")
            case "delete":
                text.append(src[i1:i2], style="deleted")
            case "insert":
                text.append(dst[j1:j2], style="inserted")
    return text


difference_theme = Theme({
    "equal": "default",
    "replaced": "dim red",
    "replacing": "green",
    "deleted": "dim red",
    "inserted": "green",
})
