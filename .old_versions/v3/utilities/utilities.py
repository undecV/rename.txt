"""Miscellaneous Utilities."""


def filenameify(string: str) -> str:
    """Make srting be a valid filename."""
    # Reference:
    # https://gist.github.com/seanh/93666
    # https://stackoverflow.com/a/62888

    return ''.join(c for c in string if c not in r'<>:"/\|?*' and c.isprintable())


def readable_size(number, suffix="B"):
    """Converts an integer into a human-readable data size unit."""
    # Reference:
    # https://stackoverflow.com/a/1094933

    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(number) < 1024.0:
            return f"{number:3.1f} {unit}{suffix}"
        number /= 1024.0
    return f"{number:.1f} Yi{suffix}"
