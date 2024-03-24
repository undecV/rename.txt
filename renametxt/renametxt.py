"""RENAME.TXT: a text-based renamer."""


import sys
import logging
import json
import enum
from typing import Any, Sequence, Mapping
from pathlib import Path
from datetime import datetime
from collections import OrderedDict

import click
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table

from renamming.renamming import RenammingItem
from renamming.string_render import string_render
from renamming.tempedit import temp_edit
from addons.addons_list import addons_list
from utilities.utilities import filenameify


logging.basicConfig(level=logging.DEBUG, format="%(message)s", handlers=(RichHandler(), ))
log = logging.getLogger()


console = Console()
print = console.print  # pylint: disable=redefined-builtin


ENCODING = "UTF-8"
EDITOR = "explorer"
CONTEXT_SETTINGS = {"help_option_names": ["--help", "-h"]}


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("items", nargs=-1, type=click.Path(file_okay=True, dir_okay=True, exists=True))
@click.option("--debug", "debug_mode", is_flag=True, show_default=True, default=False,
              help="Debug mode, print more messages.")
@click.option("-d", "--dryrun", "dryrun", is_flag=True, show_default=True, default=False,
              help="Test without executing the actual functionality.")
@click.option("-o", "--output", "output", type=click.Path(file_okay=True, dir_okay=False, writable=True),
              default=f"./{datetime.now().strftime("%Y%m%dT%H%M%S.rename.json")}",
              help="The output path of the recover log file.", show_default=True)
def main(items: list[str], debug_mode: bool, dryrun: bool, output: str):
    """RENAME.TXT: a text-based renamer."""

    # Arguments Process
    pathes: list[Path] = [Path(item).absolute() for item in items]
    output_path: Path = Path(output)

    log.debug("Argumments: \"items\" = %r", items)
    log.debug("Argumments: \"debug_mode\" = %r", debug_mode)
    log.debug("Argumments: \"dryrun\" = %r", dryrun)
    log.debug("Argumments: \"output\" = %r", output_path)

    # Generate basic variables
    renamming_items: OrderedDict[int, RenammingItem] = OrderedDict()
    for index, path in enumerate(pathes):
        variables: dict[str, Any] = {"index": index}
        renamming_item = RenammingItem(src=path, variables=variables)
        renamming_items[index] = renamming_item

    # Generate variables from addons
    for _, item in renamming_items.items():
        for addon in addons_list:
            addon_variables: dict[str, Any] = addon().get_variables(item)
            item.variables.update(addon_variables)

    # Debug mode: print table of variables
    if debug_mode:
        input_items_table = Table()
        input_items_table.add_column("Path")
        input_items_table.add_column("Variables")
        for _, item in renamming_items.items():
            input_items_table.add_row(str(item.src.name), repr(item.variables))
        print(input_items_table)

    # Build entries file
    json_lines = [[index, item.src.name] for index, item in renamming_items.items()]
    json_text = "[\n" + ",\n".join([json.dumps(line) for line in json_lines]) + "\n]\n"

    # Edit entries file
    json_text_edited = json_text
    confirm: bool = False
    reamming_items_edited: OrderedDict[int, RenammingItem] = OrderedDict()
    while not confirm:
        reamming_items_edited = OrderedDict()

        print("Opening editor...")
        json_text_edited = temp_edit(json_text_edited, EDITOR, suffix=".jsonc")

        data_edited: list[Sequence[Any]] = []
        try:
            data_edited = json.loads(json_text_edited)
            assert isinstance(data_edited, list), "Invalid format."
        except (json.JSONDecodeError, AssertionError) as exception:
            print(f"[red]Renaming text file parse error:[/red] \"{exception}\"")
            click.confirm("Continue editing?", default=True, abort=True)
            continue

        for sequence, (index, filename_edited) in enumerate(data_edited):
            item = renamming_items[index]
            item.variables["sequence"] = sequence
            filename_edited = string_render(filename_edited, item.variables)
            filename_edited = filenameify(filename_edited)
            item.dst = item.src.parent / filename_edited
            reamming_items_edited[index] = item

        print_diff(reamming_items_edited)

        if len(renamming_items) != len(reamming_items_edited):
            print("[yellow]Some entries were deleted.[/yellow]")

        dsts = [item.dst for item in reamming_items_edited.values()]
        if len(dsts) != len(set(dsts)):
            print("[red]Duplicate entries found.[/red]")
            click.confirm("Continue editing?", default=True, abort=True)
            continue

        print("[green]Duplicate entries were not found.[/green]")
        print("Please note that this is only a very basic check and does not confirm that the entry can be renamed.")

        confirm = click.confirm("Editing finished?")

    # Generate recover file
    recover_entries: list[dict[str, Any]] = []
    for index, item in reamming_items_edited.items():
        recover_entry = {
            "src": str(item.src),
            "tmp": str(item.tmp),
            "dst": str(item.dst),
        }
        recover_entries.append(recover_entry)
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_text = json.dumps(recover_entries, ensure_ascii=False, indent=4, sort_keys=False)
        output_path.write_text(output_text, encoding=ENCODING)

    # Filter
    rename_to_tmp_items: OrderedDict[int, RenammingItem] = OrderedDict()
    for index, item in reamming_items_edited.items():
        if not item.has_changed():
            continue
        rename_to_tmp_items[index] = item

    # Rename files from sorce name to temporary name.
    rename_to_dst_items = safe_batch_rename(rename_to_tmp_items, SafeBatchRenameMode.TMP, dryrun)

    # Rename files from temporary name to destination name.
    _ = safe_batch_rename(rename_to_dst_items, SafeBatchRenameMode.DST, dryrun)

    print("[green]Done.[/green]")


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
    items: OrderedDict[int, RenammingItem], mode: SafeBatchRenameMode, dryrun: bool = True
) -> OrderedDict[int, RenammingItem]:
    """
    Safely rename a truckload of files.

    Args:
        items (OrderedDict[int, RenammingItem]): An ordered dictionary containing RenammingItem instances.
        mode (SafeBatchRenameMode): The renaming mode to use (TMP or DST).
        dryrun (bool, optional): If True, performs a dry run without actually renaming the files. Defaults to True.

    Returns:
        OrderedDict[int, RenammingItem]:
            An ordered dictionary containing the successfully renamed RenammingItem instances.

    Raises:
        NotImplementedError: If an invalid mode is provided.
    """
    renamed_items: OrderedDict[int, RenammingItem] = OrderedDict()
    for index, item in items.items():
        src: Path
        dst: Path
        match mode:
            case SafeBatchRenameMode.TMP:
                src, dst = item.src, item.tmp
            case SafeBatchRenameMode.DST:
                assert item.dst is not None
                src, dst = item.tmp, item.dst
            case _:
                raise NotImplementedError
        print(f"Renameing file {index} from \"{src}\" to \"{dst}\".\n")
        try:
            if dryrun:
                pass
            else:
                src.rename(dst)
        except (FileExistsError, IsADirectoryError, NotADirectoryError, OSError) as exception:
            logging.fatal("Rename failed: \"%r\".", exception)
            continue
        renamed_items[index] = item
    return renamed_items


def print_diff(reamming_items: Mapping[int, RenammingItem]) -> None:
    """Print the differences between source and destination names in the given RenammingItem instances."""
    for index, item in reamming_items.items():
        assert item.dst is not None
        print(f"{index:04d} | {item.src.name}")
        if not item.has_changed():
            print("  [green]->[/green] | [green]Not changed.[/green]")
        else:
            print(f"  [red]->[/red] | [red]{item.dst.name}[/red]")


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        main.main(["--help"])
    else:
        main.main()
