"""Renaming utilities for the RenderRenamer."""

import json
import logging
from pathlib import Path
from copy import deepcopy
from collections import OrderedDict
from typing import Any, Sequence, Mapping
import enum

import click
from rich.text import Text
from rich.table import Table
from rich.console import Console

from render_renamer.plugins import load_plugins
from render_renamer.plugins._base import RenderRenamerAddon
from render_renamer.utilities.miscellaneous import filenameify
from .renaming_item import RenamingItem
from .temp_edit import temp_edit
from .render_string import render_string

ENCODING = "UTF-8"
EDITOR = "explorer"


console = Console()
print = console.print  # pylint: disable=redefined-builtin


logger = logging.getLogger(__name__)


def rich_table_to_text(table: Table, width: int = 120) -> Text:
    """
    Generate an ascii formatted presentation of a Rich table
    Eliminates any column styling
    """
    con = Console(width=width)
    with con.capture() as capture:
        con.print(table)
    return Text.from_ansi(capture.get())


def renaming(items: list[Path], dryrun: bool, output: Path) -> None:
    """Perform the renaming operation."""
    if not items:
        logger.warning("No input items provided, exiting.")
        return

    loaded = load_plugins()
    logger.info("Loaded plugins: %s", loaded)

    renaming_items: OrderedDict[int, RenamingItem] = OrderedDict()
    for index, path in enumerate(items):
        variables: dict[str, Any] = {"index": index}
        renaming_item = RenamingItem(src=path, variables=variables)
        renaming_items[index] = renaming_item

    # Generate variables from plugins
    for _, item in renaming_items.items():
        for plugin_cls in RenderRenamerAddon.REGISTRY.plugins():
            plugin = plugin_cls()
            plugin_variables = plugin.get_variables(item)
            item.variables.update(plugin_variables)

    logger.debug(
        "Renaming items and variables:\n%s",
        rich_table_to_text(renaming_item_variables(renaming_items))
    )

    # Build entries file
    json_lines = [[index, item.src.name]
                  for index, item in renaming_items.items()]
    json_text = "[\n" + ",\n".join([json.dumps(line, ensure_ascii=False)
                                   for line in json_lines]) + "\n]\n"

    # Edit entries file
    json_text_edited = json_text
    confirm: bool = False
    renaming_items_edited: OrderedDict[int, RenamingItem] = OrderedDict()
    while not confirm:
        renaming_items_edited = OrderedDict()

        print("Opening editor...")
        json_text_edited = temp_edit(json_text_edited, EDITOR, suffix=".jsonc")

        data_edited: list[Sequence[Any]] = []
        try:
            data_edited = json.loads(json_text_edited)
            assert isinstance(data_edited, list), "Invalid format."
        except (json.JSONDecodeError, AssertionError) as exception:
            print(
                f"[red]Renaming text file parse error:[/] \"{exception}\""
            )
            click.confirm("Continue editing?", default=True, abort=True)
            continue

        for sequence, (index, filename_edited) in enumerate(data_edited):
            item = deepcopy(renaming_items[index])
            item.variables["sequence"] = sequence

            for plugin_cls in RenderRenamerAddon.REGISTRY.plugins():
                plugin = plugin_cls()
                plugin_variables = plugin.get_variables(item)
                item.variables.update(plugin_variables)

            filename_edited = render_string(filename_edited, item.variables)
            filename_edited = filenameify(filename_edited)
            item.dst = item.src.parent / filename_edited
            renaming_items_edited[index] = item

        logger.debug(
            "Renaming items and variables:\n%s",
            rich_table_to_text(renaming_item_variables(renaming_items_edited))
        )

        print_diff(renaming_items_edited)

        if len(renaming_items) != len(renaming_items_edited):
            print("[yellow]Some entries were deleted.[/]")

        dsts = [item.dst for item in renaming_items_edited.values()]
        if len(dsts) != len(set(dsts)):
            print("[bold red on white]WARNING! Duplicate entries found.[/]")
            click.confirm("Continue editing?", default=True, abort=True)
            continue

        print("[green]Duplicate entries were not found.[/]")
        print("Please note that this is only a very basic check and does not "
              "confirm that the entry can be renamed.")

        confirm = click.confirm("Editing finished?")

    # Generate recover file
    recover_entries: list[dict[str, Any]] = []
    for index, item in renaming_items_edited.items():
        recover_entry = {
            "src": str(item.src),
            "tmp": str(item.tmp),
            "dst": str(item.dst),
        }
        recover_entries.append(recover_entry)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        doc = json.dumps(
            recover_entries, ensure_ascii=False, indent=4, sort_keys=False
        )
        output.write_text(doc, encoding=ENCODING)

    # Filter
    rename_to_tmp_items: OrderedDict[int, RenamingItem] = OrderedDict()
    for index, item in renaming_items_edited.items():
        if not item.has_changed():
            continue
        rename_to_tmp_items[index] = item

    # Rename files from source name to temporary name.
    rename_to_dst_items = safe_batch_rename(
        rename_to_tmp_items, SafeBatchRenameMode.TMP, dryrun)

    # Rename files from temporary name to destination name.
    _ = safe_batch_rename(rename_to_dst_items, SafeBatchRenameMode.DST, dryrun)

    print("[green]Done.[/]")


def renaming_item_variables(
    renaming_items: Mapping[int, RenamingItem]
) -> Table:
    """Extract variables from a RenamingItem using all registered plugins."""
    input_items_table = Table()
    input_items_table.add_column("Path")
    input_items_table.add_column("Variables")
    for _, item in renaming_items.items():
        input_items_table.add_row(str(item.src.name), repr(item.variables))
    return input_items_table


def print_diff(renaming_items: Mapping[int, RenamingItem]) -> None:
    """
    Print the differences between source and destination names in the given
    RenamingItem instances.
    """
    for index, item in renaming_items.items():
        assert item.dst is not None
        print(f"{index:04d} | {item.src.name}")
        if not item.has_changed():
            print("  [green]->[/] | [green]Not changed.[/]")
        else:
            print(f"  [red]->[/] | [red]{item.dst.name}[/]")


class SafeBatchRenameMode(enum.Enum):
    """
    Enum for specifying the renaming mode in safe_batch_rename.

    Attributes:
        TMP: Rename using temporary names.
        DST: Rename to destination names.
    """
    TMP = enum.auto()
    DST = enum.auto()


def safe_batch_rename(
    items: OrderedDict[int, RenamingItem], mode: SafeBatchRenameMode,
    dryrun: bool = True
) -> OrderedDict[int, RenamingItem]:
    """
    Safely rename a truckload of files.

    Args:
        items (OrderedDict[int, RenamingItem]): An ordered dictionary
            containing RenamingItem instances.
        mode (SafeBatchRenameMode): The renaming mode to use (TMP or DST).
        dryrun (bool, optional): If True, performs a dry run without actually
            renaming the files. Defaults to True.

    Returns:
        OrderedDict[int, RenamingItem]: An ordered dictionary containing the
            successfully renamed RenamingItem instances.

    Raises:
        NotImplementedError: If an invalid mode is provided.
    """
    renamed_items: OrderedDict[int, RenamingItem] = OrderedDict()
    for index, item in items.items():
        src: Path
        dst: Path
        match mode:
            case SafeBatchRenameMode.TMP:
                src, dst = item.src, item.tmp
            case SafeBatchRenameMode.DST:
                assert item.dst is not None
                src, dst = item.tmp, item.dst
        print(f"Renaming file {index} from \"{src}\" to \"{dst}\".")
        try:
            if dryrun:
                pass
            else:
                src.rename(dst)
        except (
            FileExistsError, IsADirectoryError, NotADirectoryError, OSError
        ) as exception:
            logging.fatal("Rename failed: \"%r\".", exception)
            continue
        renamed_items[index] = item
    return renamed_items
