"""
This module provides a function for temporary text editing using an external editor.

Note:
    - The temporary file is created using the tempfile module.
    - The edited text is returned after the user closes the editor.
"""
import subprocess
import tempfile
import click


def temp_edit(text, editor="explorer", encoding="utf-8", suffix=".txt") -> str:
    """
    Open a temporary text file in an external editor for editing.

    Args:
        text (str): The initial text to be edited.
        editor (str): The command-line command or executable for the external editor.
        encoding (str, optional): The encoding to use for the temporary file. Defaults to "utf-8".
        suffix (str, optional): The suffix for the temporary file. Defaults to ".txt".

    Returns:
        str: The edited text after the user closes the editor.

    Example:
        ```python
        edited_text = temp_edit("Hello, world!", editor="notepad.exe")
        print("Edited Text:", edited_text)
        ```

    Note:
        - The temporary file is created using the tempfile module.
        - The edited text is returned after the user closes the editor.
    """
    with tempfile.NamedTemporaryFile("w+t", encoding=encoding, suffix=suffix) as fp:
        fp.write(text)
        fp.seek(0)
        subprocess.call(f"\"{editor}\" \"{fp.name}\"")
        # os.system("pause")
        click.pause("If editing is complete, press any key...")
        fp.seek(0)
        data: str = fp.read()
    return data
