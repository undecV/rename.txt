"""Render Renamer - A tool to rename files using templates and plugins."""
import logging
from pathlib import Path
from datetime import datetime

import click
from rich.logging import RichHandler

from .renaming.renaming import renaming

logger = logging.getLogger(__name__)


def setup_logging(verbose: int = 0) -> None:
    """Configure root logger with RichHandler and the requested level.

    This is safe to call multiple times; it will replace root handlers so the
    output format is predictable when running as an installed entry point.
    """
    root = logging.getLogger()
    # determine level from verbosity
    level: int = logging.WARNING
    match verbose:
        case 0:
            level = logging.WARNING
        case 1:
            level = logging.INFO
        case _:
            level = logging.DEBUG

    root.setLevel(level)
    # replace handlers so we get Rich output when used as entrypoint
    root.handlers.clear()
    rich_handler = RichHandler(rich_tracebacks=True)
    rich_handler.setFormatter(logging.Formatter("%(message)s", datefmt="[%X]"))
    root.addHandler(rich_handler)
    logger.debug("Logging initialized: level=%s", logging.getLevelName(level))


CONTEXT_SETTINGS = {"help_option_names": ["--help", "-h"]}


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("items", nargs=-1,
                type=click.Path(file_okay=True, dir_okay=True, exists=True,
                                readable=True, writable=True, path_type=Path))
@click.option("-d", "--dryrun", "dryrun",
              is_flag=True, show_default=True, default=False,
              help="Test without executing the actual functionality.")
@click.option(
    "-o", "--output", "output",
    type=click.Path(file_okay=True, dir_okay=False,
                    readable=True, writable=True, path_type=Path),
    default=(
        Path.cwd() /
        f"{datetime.now().strftime('%Y%m%dT%H%M%S')}.rename.json"
    ),
    help="The output path of the recover log file.",
    show_default=True
)
@click.option("-v", "--verbose", count=True, default=0,
              help="Increase verbosity.")
def cli(items: list[Path], dryrun: bool, output: Path, verbose: int) -> None:
    """Render Renamer - A tool to rename files using templates and plugins."""
    setup_logging(verbose)
    logger.debug("Arguments: items=%r", items)
    logger.debug("Arguments: dryrun=%r", dryrun)
    logger.debug("Arguments: output=%r", output)
    logger.debug("Arguments: verbose=%r", verbose)

    if not items:
        print(cli.get_help(click.Context(cli)))
        return

    renaming(items=items, dryrun=dryrun, output=output)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        cli.main(["--help"])
    else:
        cli.main()
