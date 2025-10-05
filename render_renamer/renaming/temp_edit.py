"""
Module for editing text in a temporary file using an external editor.
"""
import subprocess
import tempfile
import click


def temp_edit(text, editor="explorer", encoding="utf-8", suffix=".txt") -> str:
    """
    Open a temporary file in an external editor for editing text.
    """
    with tempfile.NamedTemporaryFile(
        "w+t", encoding=encoding, suffix=suffix
    ) as file_pointer:
        file_pointer.write(text)
        file_pointer.seek(0)
        subprocess.call(f"\"{editor}\" \"{file_pointer.name}\"")
        # os.system("pause")
        click.pause("If editing is complete, press any key...")
        file_pointer.seek(0)
        data: str = file_pointer.read()
    return data
